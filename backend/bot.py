import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Car, FAQ, User, Request
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище состояния пользователя
user_states = {}

def get_db():
    return SessionLocal()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    db = get_db()
    
    # Регистрируем пользователя
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    if not user:
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name
        )
        db.add(user)
        db.commit()
    
    db.close()
    
    # Проверяем, админ ли это
    is_admin = message.from_user.id == 8496050088 # Замени на твой Telegram ID
    
    keyboard_buttons = [
        [InlineKeyboardButton(text="🚗 Каталог автомобилей", callback_data="catalog")],
        [InlineKeyboardButton(text="❓ Частые вопросы", callback_data="faq")]
    ]
    
    if is_admin:
        keyboard_buttons.append([InlineKeyboardButton(text="⚙️ Админ-панель", url="http://localhost:5174")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await message.answer(
        "👋 Добро пожаловать! Я бот для просмотра автомобилей.\n\n"
        "Выберите действие:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "catalog")
async def show_catalog(callback: types.CallbackQuery):
    db = get_db()
    cars = db.query(Car).filter(Car.is_active == True).all()
    db.close()
    
    if not cars:
        await callback.message.edit_text("🚗 Сейчас нет доступных автомобилей")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{car.title} - {car.price:,} ₽", callback_data=f"car_{car.id}")]
        for car in cars
    ])
    
    await callback.message.edit_text("🚗 Доступные автомобили:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data and c.data.startswith("car_"))
async def show_car(callback: types.CallbackQuery):
    car_id = int(callback.data.split("_")[1])
    db = get_db()
    car = db.query(Car).filter(Car.id == car_id).first()
    db.close()
    
    if not car:
        await callback.answer("Автомобиль не найден")
        return
    
    text = (
        f"🚗 {car.title}\n\n"
        f"💰 Цена: {car.price:,} ₽\n"
        f"📅 Год: {car.year}\n"
        f"📍 Пробег: {car.mileage:,} км\n"
        f"✅ Состояние: {car.condition}\n\n"
        f"📝 Описание:\n{car.description}"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📞 Оставить заявку", callback_data=f"request_{car.id}")],
        [InlineKeyboardButton(text="⬅️ Назад в каталог", callback_data="catalog")]
    ])
    
    if car.photo_url:
        await callback.message.edit_media(
            media=types.InputMediaPhoto(media=car.photo_url, caption=text),
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text(text, reply_markup=keyboard)

@dp.callback_query(lambda c: c.data and c.data.startswith("request_"))
async def request_car(callback: types.CallbackQuery):
    car_id = int(callback.data.split("_")[1])
    user_states[callback.from_user.id] = {"waiting_for_request": car_id}
    
    await callback.message.edit_text(
        "📝 Напишите свой вопрос или контактные данные для связи:\n"
        "(например: 'Интересует, звоните 8-999-123-45-67')"
    )

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    db = get_db()
    
    # Проверяем, ожидаем ли мы заявку
    if user_id in user_states and "waiting_for_request" in user_states[user_id]:
        car_id = user_states[user_id]["waiting_for_request"]
        
        # Создаем заявку
        request = Request(
            car_id=car_id,
            user_id=message.from_user.id,
            message=message.text
        )
        db.add(request)
        db.commit()
        
        del user_states[user_id]
        
        await message.answer("✅ Ваша заявка отправлена! Мы свяжемся с вами в ближайшее время.")
        db.close()
        return
    
    # Проверяем FAQ
    faqs = db.query(FAQ).all()
    for faq in faqs:
        if faq.question.lower() in message.text.lower():
            await message.answer(f"❓ {faq.answer}")
            db.close()
            return
    
    # Проверяем описание лотов
    cars = db.query(Car).filter(Car.is_active == True).all()
    for car in cars:
        car_desc = car.description.lower()
        if any(word in car_desc for word in message.text.lower().split()):
            await message.answer(f"🚗 По автомобилю {car.title}:\n{car.description}")
            db.close()
            return
    
    # Если не нашли ответ
    await message.answer(
        "😕 К сожалению, я не нашёл ответ на ваш вопрос.\n"
        "Попробуйте спросить иначе или используйте /catalog для просмотра автомобилей."
    )
    
    db.close()

@dp.callback_query(lambda c: c.data == "faq")
async def show_faq(callback: types.CallbackQuery):
    db = get_db()
    faqs = db.query(FAQ).all()
    db.close()
    
    if not faqs:
        await callback.message.edit_text("❓ Пока нет частых вопросов")
        return
    
    text = "❓ Частые вопросы:\n\n"
    for faq in faqs:
        text += f"❓ {faq.question}\n💬 {faq.answer}\n\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="start")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "start")
async def back_to_start(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚗 Каталог автомобилей", callback_data="catalog")],
        [InlineKeyboardButton(text="❓ Частые вопросы", callback_data="faq")]
    ])
    
    await callback.message.edit_text(
        "👋 Добро пожаловать! Я бот для просмотра автомобилей.\n\n"
        "Выберите действие:",
        reply_markup=keyboard
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
