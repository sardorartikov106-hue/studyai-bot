import os
import openai
import telebot

# Environment variables ishlatish (Railway-da shuni qo'shamiz)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Til tanlash tugmalari
languages = ["O'zbek", "Русский", "English"]

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for lang in languages:
        markup.add(lang)
    bot.send_message(
        message.chat.id,
        "Salom! Men Sardor yaratgan StudyAi Assistantman.\n"
        "Tilni tanlang / Выберите язык / Select language:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text in languages)
def set_language(message):
    bot.send_message(message.chat.id, f"Siz {message.text} tilini tanladingiz! Endi siz bilan AI o‘rganamiz 😎")

@bot.message_handler(func=lambda m: True)
def ai_reply(message):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Siz foydalanuvchiga yordam beradigan botsiz."},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7
        )
        answer = response.choices[0].message.content
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik yuz berdi: {str(e)}")

bot.infinity_polling()
