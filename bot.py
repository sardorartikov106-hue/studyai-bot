import telebot
import openai

TELEGRAM_TOKEN = "SENING_TELEGRAM_TOKENING"
OPENAI_API_KEY = "SENING_OPENAI_API_KEY"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# Foydalanuvchi holatini saqlash
user_language = {}

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    lang_kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    lang_kb.add("O'zbek", "Русский", "English")

    bot.send_message(
        message.chat.id,
        "Salom! Men Sardor yaratgan StudyAi Assistantman.\n"
        "Tilni tanlang:",
        reply_markup=lang_kb
    )

# ===== TIL TANLASH =====
@bot.message_handler(func=lambda m: m.text in ["O'zbek", "Русский", "English"])
def set_language(message):
    user_language[message.chat.id] = message.text

    # YANGI MENYU TUGMALARI
    menu_kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_kb.add("📚 Savol berish", "ℹ️ Yordam")

    bot.send_message(
        message.chat.id,
        f"✅ Siz {message.text} tilini tanladingiz!\n"
        "Endi menyudan foydalaning 👇",
        reply_markup=menu_kb
    )

# ===== SAVOL BERISH =====
@bot.message_handler(func=lambda m: m.text == "📚 Savol berish")
def ask_question(message):
    bot.send_message(message.chat.id, "Savolingizni yozing ✍️")

# ===== YORDAM =====
@bot.message_handler(func=lambda m: m.text == "ℹ️ Yordam")
def help_menu(message):
    bot.send_message(
        message.chat.id,
        "🤖 Men AI yordamchiman.\n"
        "Istalgan savolingni yozishing mumkin."
    )

# ===== AI JAVOB =====
@bot.message_handler(func=lambda m: True)
def ai_reply(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message.text}
            ]
        )
        answer = response.choices[0].message.content
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik: {e}")

bot.infinity_polling()
