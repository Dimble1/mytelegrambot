import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

# 🔐 Токен от BotFather и Telegram ID администратора
API_TOKEN = '8455407495:AAFVAEgYDLXS9Ph1pbuDxp9LawgxfwNF9FQ'
ADMIN_ID = 6533332698

# 📋 Клавиатура с тарифами
tariff_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔸 Тариф 1 – 100 сомов")],
        [KeyboardButton(text="🔸 Тариф 2 – 200 сомов")],
        [KeyboardButton(text="🔸 Тариф 3 – 300 сомов")],
        [KeyboardButton(text="🔸 Тариф 4 – 400 сомов")],
        [KeyboardButton(text="🔸 Тариф 5 – 500 сомов")]
    ],
    resize_keyboard=True
)

# 🚀 Инициализация бота и диспетчера
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# 🖐 Приветствие
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Просто отправьте фото и краткое описание машины, а я предложу вам варианты размещения.\n"
        "Выберите тариф ниже 👇",
        reply_markup=tariff_keyboard
    )

# 📷 Обработка фото и пересылка админу
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    caption = message.caption if message.caption else "Без описания"
    await message.answer("✅ Фото получено!\nТеперь выберите тариф для размещения.", reply_markup=tariff_keyboard)
    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=f"📥 Новая заявка:\n{caption}\n👤 От: @{message.from_user.username or 'Без username'}"
    )

# 💬 Обработка выбора тарифа и пересылка админу
@dp.message(F.text.startswith("🔸 Тариф"))
async def handle_tariff(message: types.Message):
    await message.answer(
        f"🎯 Вы выбрали: {message.text}\n\n"
        "📌 Мы разместим ваше объявление в Instagram, TikTok, Telegram и других платформах.\n"
        "Пожалуйста, ожидайте — скоро с вами свяжется администратор."
    )
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📌 Пользователь @{message.from_user.username or 'Без username'} выбрал:\n{message.text}"
    )

# 🛠 Обработка обычного текста
@dp.message(F.text)
async def handle_text(message: types.Message):
    await message.answer("📷 Пожалуйста, отправьте фото автомобиля и краткое описание.")

# 🔄 Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
