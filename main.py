import asyncio
import logging
import sys
import warnings
from playwright.async_api import async_playwright
from config import LOGIN, PASSWORD, BROWSER_LIMIT, AI_LIMIT
from ai_service import AIService
from browser_engine import BrowserEngine
from utils import load_projects

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


async def main():
    if not LOGIN or not PASSWORD:
        logger.error("❌ Логин или пароль не найдены в .env!")
        return

    projects_list = load_projects()
    if not projects_list:
        logger.error("❌ Список проектов пуст!")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        lp = await context.new_page()
        try:
            logger.info("🔐 Выполняю вход в систему...")
            await lp.goto("http://potujniygen.local/login")
            await lp.get_by_role("textbox", name="Email").fill(LOGIN)
            await lp.get_by_role("textbox", name="Password").fill(PASSWORD)
            await lp.get_by_role("button", name="Log in").click()
            await asyncio.sleep(5)
            logger.info("✅ Успешная авторизация")
        except Exception as e:
            logger.error(f"❌ Ошибка входа: {e}")
            await browser.close()
            return
        finally:
            await lp.close()

        ai_service = AIService()
        browser_semaphore = asyncio.Semaphore(BROWSER_LIMIT)
        ai_semaphore = asyncio.Semaphore(AI_LIMIT)
        engine = BrowserEngine(context, ai_service, ai_semaphore)

        tasks = []
        for proj in projects_list:
            async def sem_task(p=proj):
                async with browser_semaphore:
                    return await engine.process_project(p)

            tasks.append(sem_task())

        results = await asyncio.gather(*tasks)

        await browser.close()

        logger.info("\n" + "=" * 30 + "\nФИНАЛЬНЫЙ ОТЧЕТ\n" + "=" * 30)
        for res in results:
            logger.info(f"{res['url']:<40} | {res['status']}")


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=FutureWarning)
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info(" Программа остановлена пользователем")