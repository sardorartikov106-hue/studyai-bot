import os
import telebot
import openai

# .env dagi TOKEN va OPENAI_API_KEY ni olish
TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_API_KEY

# Start va til tanlash
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("O'zbek", "Русский", "English")
    bot.send_message(
        message.chat.id,
        "Salom! Men Sardor yaratgan StudyAi Assistantman.\n"
        "Tilni tanlang / Выберите язык / Select language:",
        reply_markup=markup
    )

# Tilni tanlash
@bot.message_handler(func=lambda m: m.text.strip().lower() in ["o'zbek", "русский", "english"])
def set_language(message):
    language = message.text.strip()
    bot.reply_to(message, f"Siz {language} tilini tanladingiz! Endi siz bilan AI o‘rganamiz 😎")

# AI javob beradigan qism
@bot.message_handler(func=lambda m: True)
def ai_response(message):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Siz foydalanuvchiga do‘stona javob beruvchi yordamchisiz."},
                {"role": "user", "content": message.text}
            ]
        )
        answer = response.choices[0].message.content
        bot.reply_to(message, answer)
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {e}")

# Botni ishga tushirish
bot.infinity_polling()
