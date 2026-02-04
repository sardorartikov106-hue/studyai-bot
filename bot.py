import os
import telebot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
