import logging
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Flask приложение
app = Flask(__name__)
bot_token = "8134896122:AAHlr-bIUi3Jo0WQdeLhgMoXwM8akp0nyFY"

# Импортируем описания
from descriptions_numbers import descriptions_numbers
from descriptions_arcana import descriptions_arcana

# Главное меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_keyboard = [["Число богатства"], ["Расчет аркана"]]
    markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Добро пожаловать! Выберите пункт меню:", reply_markup=markup)

# Функция: Число богатства
async def calculate_wealth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        number, fullname = text.split(" ", 1)

        # Преобразование числа и имени в числовое значение
        def get_sum_of_digits(num):
            while num > 9:
                num = sum(int(digit) for digit in str(num))
            return num

        def get_name_value(name):
            char_map = {'А': 1, 'И': 1, 'С': 1, 'Ъ': 1, 'Б': 2, 'Й': 2, 'Т': 2, 'Ы': 2,
                        'В': 3, 'К': 3, 'У': 3, 'Ь': 3, 'Г': 4, 'Л': 4, 'Ф': 4, 'Э': 4,
                        'Д': 5, 'М': 5, 'Х': 5, 'Ю': 5, 'Е': 6, 'Н': 6, 'Ц': 6, 'Я': 6,
                        'Ё': 7, 'О': 7, 'Ч': 7, 'Ж': 8, 'П': 8, 'Ш': 8, 'З': 9, 'Р': 9, 'Щ': 9}
            return sum(char_map.get(char.upper(), 0) for char in name)

        number_sum = get_sum_of_digits(int(number))
        name_sum = get_sum_of_digits(get_name_value(fullname))
        wealth_number = get_sum_of_digits(number_sum + name_sum)

        response = f"Ваше число богатства: {wealth_number}\n\n{descriptions_numbers.get(wealth_number, 'Описание отсутствует.')}"
        await update.message.reply_text(response)
    except ValueError:
        await update.message.reply_text("Ошибка! Введите данные в формате: 'число имя'. Пример: '22 Алексей'.")

# Функция: Расчет аркана
async def calculate_arcana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        digits = [int(char) for char in text if char.isdigit()]

        # Расчет числа аркана
        arcana_number = sum(digits)
        while arcana_number > 22:
            arcana_number = sum(int(d) for d in str(arcana_number))

        response = f"Ваш аркан: {arcana_number}\n\n{descriptions_arcana[arcana_number]}"
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text("Ошибка! Введите число в правильном формате.")

# Обработка выбора в меню
async def menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    if choice == "Число богатства":
        await update.message.reply_text("Введите данные в формате: 'число имя'. Пример: '22 Алексей'")
    elif choice == "Расчет аркана":
        await update.message.reply_text("Введите дату в формате ДД.ММ.ГГГГ")
    else:
        await update.message.reply_text("Пожалуйста, выберите пункт из меню.")

if __name__ == "__main__":
    application = ApplicationBuilder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^\d+ \w+"), calculate_wealth))
    application.add_handler(MessageHandler(filters.Regex("^\d{2}\.\d{2}\.\d{4}$"), calculate_arcana))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_choice))
    application.run_polling()
