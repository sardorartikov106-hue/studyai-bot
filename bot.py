import telebot
import os

TOKEN = os.getenv("TOKEN")  # .env dagi TOKEN ni oladi
bot = telebot.TeleBot(TOKEN)

# Start va til tanlash qismi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("O'zbek", "Русский", "English")
    bot.send_message(message.chat.id, 
                     "Salom! Men Sardor yaratgan StudyAi Assistantman.\n"
                     "Tilni tanlang / Выберите язык / Select language:", 
                     reply_markup=markup)

@bot.message_handler(func=lambda m: m.text.strip().lower() in ["o'zbek", "русский", "english"])
def set_language(message):
    language = message.text.strip()
    bot.reply_to(message, f"Siz {language} tilini tanladingiz! Endi siz bilan AI o‘rganamiz 😎")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"Siz yozdingiz: {message.text}\n(Endi AI bu yerda javob beradi)")

bot.infinity_polling()
