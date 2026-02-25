import asyncio
import re
import logging
from playwright.async_api import Page, BrowserContext
from config import ALL_PAGES, AI_TARGET_PAGES, TEXT_TEMPLATES

logger = logging.getLogger(__name__)


class BrowserEngine:
    def __init__(self, context: BrowserContext, ai_service, ai_sem):
        self.context = context
        self.ai = ai_service
        self.ai_sem = ai_sem

    async def process_project(self, project: dict):
        url = project["url"]
        curr = project["curr"]
        page = await self.context.new_page()

        try:
            logger.info(f"СТАРТ [{curr}]: {url}")
            await page.goto(url, timeout=90000)
            await asyncio.sleep(4)

            await self._ensure_content_generated(page, url)

            for p_name in ALL_PAGES:
                try:
                    await self._process_single_page(page, p_name, curr, url)
                except Exception as e:
                    logger.warning(f"Ошибка на странице {p_name} ({url}): {e}")

            await page.locator("button:has-text('Зберегти'), input[value='Зберегти']").first.click()
            await page.wait_for_load_state("networkidle", timeout=60000)
            logger.info(f"✅ УСПЕХ: {url}")
            return {"url": url, "status": "✅ OK"}

        except Exception as e:
            logger.error(f"❌ КРИТИЧЕСКАЯ ОШИБКА {url}: {e}")
            return {"url": url, "status": f"❌ ERROR: {str(e)[:50]}"}
        finally:
            await page.close()

    async def _ensure_content_generated(self, page: Page, url: str):
        while True:
            idx = page.get_by_text("Index", exact=True).first
            if await idx.is_visible(): await idx.click()
            await asyncio.sleep(3)

            char_count = await page.evaluate("() => document.querySelector('.note-editable')?.innerText.length || 0")
            if char_count > 100:
                break

            logger.info(f"Сайт {url[-5:]} пустой. Генерирую...")
            gen_btn = page.locator("button:has-text('Згенерувати сайт')").first
            if await gen_btn.is_visible():
                await gen_btn.click()
                await asyncio.sleep(2)
                ai_cb = page.locator("label:has-text('AI Контент')").locator("input[type='checkbox']")
                if await ai_cb.count() > 0: await ai_cb.check()
                await page.locator("button:has-text('Підтвердити')").click()

            await asyncio.sleep(305)
            await page.reload()
            await asyncio.sleep(5)

    async def _process_single_page(self, page: Page, p_name: str, curr: str, url: str):
        menu_link = page.get_by_text(p_name, exact=True).first
        if not await menu_link.is_visible():
            return

        await menu_link.click()
        await asyncio.sleep(3)

        if p_name in AI_TARGET_PAGES:
            await self._handle_ai_page(page, curr)
        else:
            await self._handle_standard_page(page, p_name, curr)

    async def _handle_ai_page(self, page: Page, curr: str):
        content_block = page.locator("div").filter(has_text="Content").filter(has=page.locator(".btn-codeview")).first
        if await content_block.count() == 0:
            content_block = page.locator(".note-editor").first

        code_view_btn = content_block.locator(".btn-codeview").first
        is_active = await code_view_btn.get_attribute("class")

        if not is_active or "active" not in is_active:
            await code_view_btn.click()
            await asyncio.sleep(2)

        textarea = content_block.locator('textarea.note-codable').first
        if await textarea.count() == 0: textarea = content_block.locator('textarea').first

        if await textarea.count() > 0:
            current_html = await textarea.input_value()
            if "Do not explain yourself" in current_html:
                await code_view_btn.click()
            elif len(current_html) > 50:
                regex_curr = r"([$€£₴¥]|\blei\b|\bzl\b|\beuro\b)"
                processed_html = re.sub(regex_curr, curr, current_html, flags=re.IGNORECASE)

                async with self.ai_sem:
                    final_html = await self.ai.fix_html(processed_html)

                await textarea.click()
                await page.keyboard.press("Control+A")
                await page.keyboard.press("Backspace")
                await page.keyboard.insert_text(final_html)
                await asyncio.sleep(1)
                await code_view_btn.click()
            else:
                await code_view_btn.click()

    async def _handle_standard_page(self, page: Page, p_name: str, curr: str):
        await page.evaluate(f"""([p, tc, b4, b5, app, c]) => {{
            const regex = /([$€£₴¥]|\\blei\\b|\\bzl\\b|\\beuro\\b)/gi;
            const inject = (title, html) => {{
                const headers = Array.from(document.querySelectorAll('div, b, span, h2, h3'))
                                         .filter(el => el.innerText.trim() === title);
                const target = headers[headers.length - 1];
                if (target) {{
                    const container = target.closest('.mb-6') || target.parentElement.parentElement;
                    const codeBtn = container.querySelector('.btn-codeview');
                    const textarea = container.querySelector('textarea.note-codable, textarea');
                    if (codeBtn && textarea) {{
                        if (!codeBtn.classList.contains('active')) codeBtn.click();
                        textarea.value = html.replace(regex, c);
                        textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        setTimeout(() => {{ if (codeBtn) codeBtn.click(); }}, 400);
                    }}
                }}
            }};
            if (p === "Bonuses") {{
                inject("H2 - 4", b4);
                setTimeout(() => inject("H2 - 5", b5), 1000);
            }} else if (p === "Casino App") {{
                inject("H2 - 2", app);
            }}
            document.querySelectorAll('.note-editable').forEach(ed => {{
                ed.innerHTML = ed.innerHTML.replace(regex, c);
            }});
        }}""", [p_name, TEXT_TEMPLATES["TC_4"], TEXT_TEMPLATES["BONUS_H2_4"],
                TEXT_TEMPLATES["BONUS_H2_5"], TEXT_TEMPLATES["CASINO_APP_H2_2"], curr])