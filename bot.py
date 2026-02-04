import telebot

# ⬇️ SHU IKKITA JOYGA O'ZING QO'YASAN
TELEGRAM_TOKEN = 8524493737:AAEiCQGdNtY7iUIpOBDwgS7deQM7FPZElsw
OPENAI_API_KEY = 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

bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_state = {}

@bot.message_handler(commands=['start'])
def start(message):
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("O'zbek", "Русский", "English")
    user_state[message.chat.id] = "lang"

    bot.send_message(
        message.chat.id,
        "👉 TUGMADAN BOSIB tilni tanla:",
        reply_markup=kb
    )

@bot.message_handler(func=lambda m: True)
def handler(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if user_state.get(chat_id) == "lang":
        if text in ["O'zbek", "Русский", "English"]:
            user_state[chat_id] = "menu"

            menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            menu.add("📚 Savol berish")
            menu.add("ℹ️ Yordam")

            bot.send_message(
                chat_id,
                f"✅ {text} tili tanlandi",
                reply_markup=menu
            )
        else:
            bot.send_message(chat_id, "❌ Iltimos, tugmadan tanla")
        return

    if text == "📚 Savol berish":
        bot.send_message(chat_id, "Savolingni yoz ✍️")
        return

    if text == "ℹ️ Yordam":
        bot.send_message(chat_id, "Men StudyAi botman 🤖")
        return

    bot.send_message(chat_id, f"Siz yozdingiz: {text}")

bot.infinity_polling()
