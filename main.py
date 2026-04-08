import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "8081179294:AAG3yTPPyrEFSTJo5Z-4Pz3kRm583z2vdu4"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# [ВСТАВЬ СЮДА ВЕСЬ КОД КЛАВИАТУР И ХЕНДЛЕРОВ ИЗ ПРЕДЫДУЩЕГО ОТВЕТА]
# ... (промт, функции kb_*, хендлеры) ...

# 🌐 Веб-сервер для "пробуждения" бота на Render
async def handle_health(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get('/', handle_health)

async def start_webserver():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logging.info("Webserver started on port 8080")

# 🚀 Запуск
async def main():
    await start_webserver()  # Запускаем веб-сервер
    await dp.start_polling(bot)  # Запускаем бота

if __name__ == "__main__":
    asyncio.run(main())