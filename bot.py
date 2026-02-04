import telebot

TELEGRAM_TOKEN = "TELEGRAM_TOKENINGNI_BU_YERGA_QOY"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_step = {}

# ===== /start =====
@bot.message_handler(commands=['start'])
def start(message):
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("O'zbek", "Русский", "English")

    user_step[message.chat.id] = "language"

    bot.send_message(
        message.chat.id,
        "Tilni tanlang:",
        reply_markup=kb
    )

# ===== TIL TANLASH =====
@bot.message_handler(func=lambda m: user_step.get(m.chat.id) == "language")
def choose_language(message):
    if message.text not in ["O'zbek", "Русский", "English"]:
        bot.send_message(message.chat.id, "Iltimos, tugmadan tanlang 👇")
        return

    user_step[message.chat.id] = "menu"

    menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add("📚 Savol berish")
    menu.add("ℹ️ Yordam")

    bot.send_message(
        message.chat.id,
        f"✅ {message.text} tili tanlandi",
        reply_markup=menu
    )

# ===== SAVOL BERISH =====
@bot.message_handler(func=lambda m: m.text == "📚 Savol berish")
def ask(message):
    user_step[message.chat.id] = "ask"
    bot.send_message(message.chat.id, "Savolingni yoz ✍️")

# ===== YORDAM =====
@bot.message_handler(func=lambda m: m.text == "ℹ️ Yordam")
def help_cmd(message):
    bot.send_message(message.chat.id, "Men StudyAi botman 🤖")

# ===== ODDIY JAVOB (ENG OXIRIDA!) =====
@bot.message_handler(func=lambda m: True)
def fallback(message):
    if user_step.get(message.chat.id) == "ask":
        bot.send_message(message.chat.id, f"🧠 AI javobi:\n{message.text}")
    else:
        bot.send_message(message.chat.id, "Menyudan foydalan 👇")

bot.infinity_polling()
