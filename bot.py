import telebot
import openai

# --- TOKEN va API kalitini shu yerga qo'shasiz ---
TELEGRAM_TOKEN = "8524493737:AAEiCQGdNtY7iUIpOBDwgS7deQM7FPZElsw"
OPENAI_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# --- Til tanlash va start qismi ---
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

# --- Tilni tanlagan foydalanuvchi ---
@bot.message_handler(func=lambda m: m.text.strip().lower() in ["o'zbek", "русский", "english"])
def set_language(message):
    language = message.text.strip()
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("AI bilan savol berish")  # Misol uchun yangi tugma
    bot.send_message(message.chat.id, f"Siz {language} tilini tanladingiz! Endi siz bilan AI o‘rganamiz 😎", reply_markup=markup)

# --- AI javobi ---
@bot.message_handler(func=lambda m: True)
def chat_with_ai(message):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        answer = response.choices[0].message.content
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik yuz berdi: {e}")

# --- Botni ishga tushurish ---
bot.infinity_polling()
