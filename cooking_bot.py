import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, CallbackContext

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8496448297:AAH-3Mi2MJ0xRWel4eURTki2HbgK66XOsW4')

# Ваши рецепты
RECIPES = {
    "Завтрак": {
        "Горячее": [
            {
                "name": "🍳 Омлет с сыром",
                "ingredients": ["Яйца - 3 шт.", "Молоко - 50 мл", "Сыр - 50 г", "Соль, перец"],
                "recipe": "1. Взбейте яйца с молоком\n2. Натрите сыр\n3. Разогрейте сковороду\n4. Жарьте 5-7 минут под крышкой"
            }
        ]
    },
    "Обед": {
        "Горячее": [
            {
                "name": "🍜 Куриный суп",
                "ingredients": ["Куриное филе - 200 г", "Вода - 1.5 л", "Лапша - 100 г", "Морковь - 1 шт.", "Лук - 1 шт."],
                "recipe": "1. Сварите куриный бульон\n2. Добавьте нарезанные овощи\n3. Варите до готовности"
            }
        ]
    },
    "Десерты": {
        "Выпечка": [
            {
                "name": "🥕 Морковный кекс",
                "ingredients": ["Мука - 2 кружки", "Сахар - 1 кружка", "Морковь - 2 шт.", "Яйца - 3 шт.", "Масло - 2/3 кружки"],
                "recipe": "1. Натрите морковь\n2. Смешайте все ингредиенты\n3. Выпекайте 50-60 минут при 180°C"
            }
        ]
    }
}

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🍳 Завтрак", callback_data='Завтрак')],
        [InlineKeyboardButton("🍲 Обед", callback_data='Обед')],
        [InlineKeyboardButton("🍰 Десерты", callback_data='Десерты')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Привет! Я твой кулинарный помощник! Выбери категорию:', reply_markup=reply_markup)

def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    message = query.message

    if data in ['Завтрак', 'Обед', 'Десерты']:
        dish_types = list(RECIPES[data].keys())
        keyboard = []
        for dish_type in dish_types:
            keyboard.append([InlineKeyboardButton(dish_type, callback_data=f'тип_{data}_{dish_type}')])
        keyboard.append([InlineKeyboardButton("🔙 В главное меню", callback_data='main_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.edit_text(text=f"🍽️ {data}. Выбери категорию блюд:", reply_markup=reply_markup)

    elif data == 'main_menu':
        keyboard = [
            [InlineKeyboardButton("🍳 Завтрак", callback_data='Завтрак')],
            [InlineKeyboardButton("🍲 Обед", callback_data='Обед')],
            [InlineKeyboardButton("🍰 Десерты", callback_data='Десерты')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.edit_text(text='👨‍🍳 Выбери категорию:', reply_markup=reply_markup)

    elif data.startswith('тип_'):
        parts = data.split('_')
        meal_type, dish_type = parts[1], parts[2]
        dishes = RECIPES[meal_type][dish_type]
        
        keyboard = []
        for index, dish in enumerate(dishes):
            keyboard.append([InlineKeyboardButton(dish['name'], callback_data=f'блюдо_{meal_type}_{dish_type}_{index}')])
        keyboard.append([InlineKeyboardButton("🔙 Назад к категориям", callback_data=meal_type)])
        keyboard.append([InlineKeyboardButton("🔙 В главное меню", callback_data='main_menu')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.edit_text(text=f"📋 {meal_type}, {dish_type}. Выбери блюдо:", reply_markup=reply_markup)

    elif data.startswith('блюдо_'):
        parts = data.split('_')
        meal_type, dish_type, dish_index = parts[1], parts[2], int(parts[3])
        dish = RECIPES[meal_type][dish_type][dish_index]

        recipe_text = f"🍳 <b>{dish['name']}</b>\n\n"
        recipe_text += "📋 <u>Ингредиенты:</u>\n"
        for ingredient in dish['ingredients']:
            recipe_text += f"• {ingredient}\n"
        recipe_text += f"\n👩‍🍳 <u>Рецепт:</u>\n{dish['recipe']}"

        keyboard = [
            [InlineKeyboardButton("🔙 Назад к списку", callback_data=f'тип_{meal_type}_{dish_type}')],
            [InlineKeyboardButton("🔙 В главное меню", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.edit_text(text=recipe_text, reply_markup=reply_markup, parse_mode='HTML')

def main():
    # Используем Updater вместо Application для совместимости
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_click))
    
    print("✅ Бот запущен! Напишите /start в Телеграме")
    
    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
