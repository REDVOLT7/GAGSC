import os
import asyncio
from telethon.sync import TelegramClient
from telethon import Button
from telegram import Bot

# Загружаем переменные из окружения
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
TELEGRAM_BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['YOUR_CHAT_ID']

session_name = 'gag_userbot'
TARGET_BOT = 'Grow_A_GardenStockBot'

KEYWORDS = [
    "Ember Lily", "Beanstalk", "Mushroom",
    "Cacao", "Master Sprinkler", "Friendship pot", "Bug Egg", "Lighting rod", "Mythical Egg"
]

tg_bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def monitor_stock():
    async with TelegramClient(session_name, api_id, api_hash) as client:
        await client.send_message(TARGET_BOT, "/start")
        await asyncio.sleep(1)

        async for message in client.iter_messages(TARGET_BOT, limit=5):
            if message.buttons:
                for row in message.buttons:
                    for button in row:
                        if "Стоки" in button.text:
                            try:
                                await button.click()
                                await asyncio.sleep(3)
                                raise StopAsyncIteration
                            except Exception as e:
                                print("🚨 Ошибка при клике:", e)
                break

        async for new_message in client.iter_messages(TARGET_BOT, limit=1):
            text = new_message.text
            found = [kw for kw in KEYWORDS if kw.lower() in text.lower()]

            if found:
                alert = "🔔 Найдено:\n" + "\n".join(f"• {kw}" for kw in found)
                await tg_bot.send_message(chat_id=CHAT_ID, text=alert + "\n\n📦 Сток:\n" + text)
                print("🔔 Отправлено:", found)
            else:
                print("❌ Нет нужных предметов.")

async def loop():
    while True:
        try:
            await monitor_stock()
        except Exception as e:
            print("🚨 Общая ошибка:", e)
        await asyncio.sleep(300)

asyncio.run(loop())