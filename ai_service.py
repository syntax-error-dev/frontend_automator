import asyncio
import google.generativeai as genai
import logging
from config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    async def fix_html(self, dirty_html: str) -> str:
        if not dirty_html or len(dirty_html) < 20:
            return dirty_html

        prompt = f"""
            Ты HTML валидатор. Твоя задача - исправить сломанную HTML разметку так чтоб она выглядела идеально в любом случае.
            ПРАВИЛА:
            1. Исправь незакрытые теги, вложенность списков (ul, ol, li).
            2. Убери лишние пустые теги.
            3. СТРОГО ЗАПРЕЩЕНО менять текст внутри тегов. Оставь текст, цифры и символы как есть.
            4. Верни ТОЛЬКО чистый HTML код. Не используй markdown блоки.
            5. Ты можешь пользоваться тегами ul, ol, li, strong, br, p.
            6. если есть теги кроме ul, ol, li, strong, br, p - удаляем их.
            7. Если в тексте ты встретишь плейсхолдер [] с любым значением, кроме [Casino Name] - удаляешь его по контексту, возможно с ближайшим параграфом или пунктом в списке, главное чтоб было даже непонятно что там что-то должно быть.
            8. Ты можешь пользоваться только html, больше ничего использовать нельзя.
            9. использовать тег <p> внутри списка можно только так чтоб текст не переносило на новую строку
            10. если по контексту должен быть заголовок - делаешь его жирным шрифтом, потом <br> и потом <p>
            11. Если в тексте есть ссылка на почту (например, support@...) или любая другая активная ссылка - ты ее удаляешь по контексту, как будто бы ее там е должно быть.

        Вот HTML код:
        {dirty_html}
        """


        for attempt in range(5):
            try:
                response = await asyncio.to_thread(self.model.generate_content, prompt)
                return response.text.replace("```html", "").replace("```", "").strip()
            except Exception as e:
                wait_time = (attempt + 1) * 5
                logger.warning(f"AI Error (attempt {attempt+1}): {e}. Waiting {wait_time}s")
                await asyncio.sleep(wait_time)
        return dirty_html