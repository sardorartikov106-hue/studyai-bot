import telebot
import openai
from telebot import types

TELEGRAM_TOKEN = "8524493737:AAEiCQGdNtY7iUIpOBDwgS7deQM7FPZElsw"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_languages = {}

# Start va til tanlash
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("O'zbek", "Русский", "English")
    bot.send_message(
        message.chat.id,
        "Salom! Men Sardor yaratgan StudyAi Assistantman.\nTilni tanlang / Выберите язык / Select language:",
        reply_markup=markup
    )

# Til tanlanganida
@bot.message_handler(func=lambda m: m.text.strip() in ["O'zbek", "Русский", "English"])
def set_language(message):
    language = message.text.strip()
    user_languages[message.chat.id] = language
    
    # Keyboardni olib tashlash
    remove_markup = types.ReplyKeyboardRemove()
    bot.send_message(
        message.chat.id,
        f"Siz {language} tilini tanladingiz! Endi siz bilan AI o‘rganamiz 😎",
        reply_markup=remove_markup
    )

# AI javob berish
@bot.message_handler(func=lambda m: True)
def ai_reply(message):
    if message.chat.id not in user_languages:
        bot.send_message(message.chat.id, "Iltimos, avval tilni tanlang.")
        return
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Siz foydalanuvchi bilan {user_languages[message.chat.id]} tilida gaplashadigan yordamchi AI botisiz."},
                {"role": "user", "content": message.text}
            ]
        )
        answer = response.choices[0].message.content
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik yuz berdi: {e}")

bot.infinity_polling()
