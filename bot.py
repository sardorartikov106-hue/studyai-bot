import telebot
from openai import OpenAI

# Telegram va OpenAI kalitlari
TELEGRAM_TOKEN = "8524493737:AAEiCQGdNtY7iUIpOBDwgS7deQM7FPZElsw"
OPENAI_API_KEY = "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"

# OpenAI client yaratish
client = OpenAI(api_key=OPENAI_API_KEY)

# Telegram bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Foydalanuvchi tillarini saqlash (chat_id => language)
user_languages = {}

# Til tanlash tugmalari
language_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
language_markup.add("O'zbek", "Русский", "English")

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Salom! Men Sardor yaratgan StudyAi Assistantman.\n"
        "Tilni tanlang / Выберите язык / Select language:",
        reply_markup=language_markup
    )

@bot.message_handler(func=lambda m: m.text.strip() in ["O'zbek", "Русский", "English"])
def set_language(message):
    language = message.text.strip()
    user_languages[message.chat.id] = language
    bot.send_message(message.chat.id, f"Siz {language} tilini tanladingiz! Endi siz bilan AI o‘rganamiz 😎")

@bot.message_handler(func=lambda m: True)
def chat_with_ai(message):
    # Foydalanuvchi hali til tanlamagan bo‘lsa default O'zbek
    language = user_languages.get(message.chat.id, "O'zbek")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        answer = response.choices[0].message.content
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik yuz berdi: {e}")

bot.infinity_polling()
