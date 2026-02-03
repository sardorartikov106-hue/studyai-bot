import telebot
import openai

# Shu yerga o'zingizning token va OpenAI API kalitingizni qo'ying
TELEGRAM_TOKEN = "8524493737:AAEiCQGdNtY7iUIpOBDwgS7deQM7FPZElsw"
OPENAI_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# Til tanlash tugmalari
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("O'zbek", "Русский", "English")
    bot.send_message(
        message.chat.id,
        "Salom! Men Sardor yaratgan StudyAi Assistantman.\nTilni tanlang / Выберите язык / Select language:",
        reply_markup=markup
    )

# Tilni tanlash
@bot.message_handler(func=lambda m: m.text.strip().lower() in ["o'zbek", "русский", "english"])
def set_language(message):
    language = message.text.strip()
    bot.reply_to(message, f"Siz {language} tilini tanladingiz! Endi siz bilan AI o‘rganamiz 😎")

# AI bilan javob berish
@bot.message_handler(func=lambda m: True)
def ai_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        answer = response['choices'][0]['message']['content']
        bot.reply_to(message, answer)
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {e}")

bot.infinity_polling()
