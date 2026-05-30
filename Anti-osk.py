import logging
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ChatPermissions
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from groq import Groq

# --- КОНФИГУРАЦИЯ ---
TELEGRAM_TOKEN = "СЮДА_СВОЙ_ТОКЕН"
GROQ_API_KEY = "СЮДА_СВОЙ_КЛЮЧ"

# Список имен для проверки
TARGET_NAMES = ["актерев", "шгш"]

# Инициализация
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
client = Groq(api_key=GROQ_API_KEY)

# Функция проверки через ИИ
async def is_insult(text):
    prompt = (f"Проанализируй текст: '{text}'. "
              f"Содержит ли это сообщение оскорбление в адрес участников шгш? "
              f"Ответь строго одним словом: ДА или НЕТ.")
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile", # Быстрая модель от Groq
    )
    
    answer = chat_completion.choices[0].message.content.strip().upper()
    return "ДА" in answer

@dp.message(F.text)
async def moderation(message: types.Message):
    text_lower = message.text.lower()
    
    # Сначала проверяем, есть ли вообще упоминание имен в тексте
    if any(name in text_lower for name in TARGET_NAMES):
        if await is_insult(message.text):
            try:
                ban_duration = int(time.time()) + 86400 
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=ban_duration
                )
                
                await message.reply("Нарушение правил: оскорбление. Пользователь замучен на 24 часа.")
            except TelegramBadRequest as e:
                print(f"Не удалось выдать мут: {e}")
if __name__ == "__main__":
    dp.run_polling(bot)
