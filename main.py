import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ⚙️ Токен бота
TOKEN = "8081179294:AAG3yTPPyrEFSTJo5Z-4Pz3kRm583z2vdu4"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🎨 Твой промт для кнопки "Промт"
PROMPT_TEXT = """[ТУТ СОН], highly detailed, cinematic masterpiece, ultra realistic or stylized trending digital art, vibrant colors, perfect lighting, volumetric light, depth of field, атмосферное освещение, мягкие тени, реалистичные отражения, 4k, sharp focus
dynamic composition, strong subject focus, visually striking, aesthetically perfect, storytelling scene, immersive, rich details, no clutter
vertical 9:16 composition, perfectly centered, balanced framing, subject clearly visible, background supporting the scene
ADD TEXT AT BOTTOM CENTER:
"Dream: ТУТ СОН"
elegant modern typography, cinematic font, glowing gradient (orange to pink or neon depending on scene), soft light outline, high readability, clean, centered, с отступами от краёв, не перекрывает главный объект
perfect lighting balance between subject and text, harmonious colors, visually pleasing, viral social media style, trending, high engagement, masterpiece"""

# 🔘 КЛАВИАТУРЫ
def main_menu():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="🖼 Изображение", callback_data="menu_image"))
    kb.add(InlineKeyboardButton(text="🎬 Видео", callback_data="menu_video"))
    kb.add(InlineKeyboardButton(text="✂️ Редактор Видео", callback_data="menu_editor"))
    kb.add(InlineKeyboardButton(text="🎵 Музыка", callback_data="menu_music"))
    kb.add(InlineKeyboardButton(text="💡 Полезное", callback_data="menu_useful"))
    return kb.as_markup()

def back_kb(callback: str):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="🔙 Назад", callback_data=callback))
    return kb.as_markup()

# 🖼 Меню: Изображение
def kb_image():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="GPT", url="https://chatgpt.com/ru-RU/"))
    kb.add(InlineKeyboardButton(text="Акулы", url="https://myneuralnetworks.ru/generating_images_from_text/"))
    kb.add(InlineKeyboardButton(text="Леонардо", url="https://leonardo.ai/"))
    kb.add(InlineKeyboardButton(text="📝 Промт", callback_data="show_prompt"))
    kb.adjust(2)
    kb.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    return kb.as_markup()

# 🎬 Меню: Видео
def kb_video():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Digen", url="https://digen.ai/ru/space/460578"))
    kb.add(InlineKeyboardButton(text="Pollo", url="https://pollo.ai/ru"))
    kb.add(InlineKeyboardButton(text="Kling", url="https://kling.ai/"))
    kb.add(InlineKeyboardButton(text="📧 Почта", url="https://temp-mail.org/en/"))
    kb.adjust(2)
    kb.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    return kb.as_markup()

# ✂️ Меню: Редактор
def kb_editor():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Обрезать", url="https://online-video-cutter.com/ru/resize-video"))
    kb.add(InlineKeyboardButton(text="Сжать", url="https://www.video2edit.com/ru/resize-video"))
    kb.add(InlineKeyboardButton(text="Кадр", url="https://batchtools.pro/ru/videoframes"))
    kb.add(InlineKeyboardButton(text="Водяной знак", url="https://ezremove.ai/ru/video-watermark-remover/"))
    kb.adjust(2)
    kb.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    return kb.as_markup()

# 🎵 Меню: Музыка
def kb_music():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="🎼 Музыка", url="https://myneuralnetworks.ru/music_generator"))
    kb.add(InlineKeyboardButton(text="🗣 Речь", url="https://myneuralnetworks.ru/tts"))
    kb.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    return kb.as_markup()

# 💡 Меню: Полезное (с подменю)
def kb_useful():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Кросспостинг", callback_data="useful_cross"))
    kb.add(InlineKeyboardButton(text="Автоматизация", callback_data="useful_auto"))
    kb.add(InlineKeyboardButton(text="Идея", callback_data="useful_idea"))
    kb.add(InlineKeyboardButton(text="ИИ Аватар", callback_data="useful_avatar"))
    kb.add(InlineKeyboardButton(text="Озвучка", callback_data="useful_voice"))
    kb.add(InlineKeyboardButton(text="Монтаж", callback_data="useful_edit"))
    kb.add(InlineKeyboardButton(text="Обложка", callback_data="useful_cover"))
    kb.adjust(2)
    kb.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    return kb.as_markup()

# 🔙 Кнопка назад в главное меню
def kb_back_main():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    return kb.as_markup()

# 📄 Тексты для подменю "Полезное"
USEFUL_TEXTS = {
    "useful_cross": "https://publish.buffer.com/schedule - 3 канала на бесплатке\nhttps://postmypost.io/ru/\nhttps://smmplanner.com/",
    "useful_auto": "https://n8n.io/\nhttps://www.make.com/en - для начала",
    "useful_idea": "https://rekreate.ai/ - идеи для контента Ру\nhttps://getvamos.ai/ - идеи для контента\nhttps://claude.com/app-unavailable-in-region\nhttps://www.deepseek.com/",
    "useful_avatar": "https://www.heygen.com/ - Рекомендашка\nhttps://www.hedra.com/\nhttps://www.d-id.com/",
    "useful_voice": "https://help.elevenlabs.io/hc/en-us\nhttps://murf.ai/",
    "useful_edit": "https://captions.ai/ - Популярная\nhttps://www.submagic.co/\nhttps://www.opus.pro/\nhttps://klap.app/ - рекомендашка\n\n+ Видеовставки (Sora - рекомендашка, Krea, Veo)",
    "useful_cover": "https://www.midjourney.com/ - Популярный\nhttps://leonardo.ai/\nhttps://www.krea.ai/ - рекомендашка\nhttps://ideogram.ai/"
}

# 🚀 ХЕНДЛЕРЫ
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Привет! Выбери раздел:", reply_markup=main_menu())

@dp.callback_query(F.data == "main_menu")
async def go_main(call: types.CallbackQuery):
    await call.message.edit_text("👋 Главное меню:", reply_markup=main_menu())

# 🖼 Изображение
@dp.callback_query(F.data == "menu_image")
async def show_image(call: types.CallbackQuery):
    await call.message.edit_text("🖼 Инструменты для изображений:", reply_markup=kb_image())

@dp.callback_query(F.data == "show_prompt")
async def send_prompt(call: types.CallbackQuery):
    await call.message.answer(PROMPT_TEXT, reply_markup=kb_back_main())
    await call.answer()

# 🎬 Видео
@dp.callback_query(F.data == "menu_video")
async def show_video(call: types.CallbackQuery):
    await call.message.edit_text("🎬 Сервисы для видео:", reply_markup=kb_video())

# ✂️ Редактор
@dp.callback_query(F.data == "menu_editor")
async def show_editor(call: types.CallbackQuery):
    await call.message.edit_text("✂️ Редакторы видео:", reply_markup=kb_editor())

# 🎵 Музыка
@dp.callback_query(F.data == "menu_music")
async def show_music(call: types.CallbackQuery):
    await call.message.edit_text("🎵 Генерация аудио:", reply_markup=kb_music())

# 💡 Полезное + подменю
@dp.callback_query(F.data == "menu_useful")
async def show_useful(call: types.CallbackQuery):
    await call.message.edit_text("💡 Полезные инструменты:", reply_markup=kb_useful())

@dp.callback_query(F.data.startswith("useful_"))
async def show_useful_sub(call: types.CallbackQuery):
    key = call.data
    if key in USEFUL_TEXTS:
        await call.message.answer(USEFUL_TEXTS[key], reply_markup=kb_back_main())
        await call.answer()

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

# 🏁 Запуск
async def main():
    await start_webserver()  # Запускаем веб-сервер
    await dp.start_polling(bot)  # Запускаем бота

if __name__ == "__main__":
    asyncio.run(main())