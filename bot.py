import telebot
import openai

# -----------------------------
# TOKEN va OpenAI API kaliti
# -----------------------------
TELEGRAM_TOKEN = "8524493737:AAEiCQGdNtY7iUIpOBDwgS7deQM7FPZElsw"
OPENAI_API_KEY = "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"

# OpenAI ni sozlash
openai.api_key = OPENAI_API_KEY

# Telegram bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# -----------------------------
# Start va til tanlash
# -----------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("O'zbek", "Русский", "English")
    bot.send_message(
        message.chat.id, 
        "Salom! Men Sardor yaratgan StudyAi Assistantman.\nTilni tanlang / Выберите язык / Select language:", 
        reply_markup=markup
    )

# Tilni saqlash va javob berish
user_languages = {}

@bot.message_handler(func=lambda m: m.text.strip() in ["O'zbek", "Русский", "English"])
def set_language(message):
    language = message.text.strip()
    user_languages[message.chat.id] = language
    bot.send_message(message.chat.id, f"Siz {language} tilini tanladingiz! Endi siz bilan AI o‘rganamiz 😎")

# AI bilan chat
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

# Botni ishga tushurish
bot.infinity_polling()
