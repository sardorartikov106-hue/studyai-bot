import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from openai import OpenAI

# ====== TOKENLARNI SHU YERGA QO'YASAN ======
TELEGRAM_TOKEN = "BU_YERGA_TELEGRAM_TOKEN"
OPENAI_API_KEY = "BU_YERGA_OPENAI_API_KEY"
# =========================================

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

user_lang = {}

# /start
@bot.message_handler(commands=["start"])
def start(message):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🇺🇿 O‘zbekcha", callback_data="lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
    )
    bot.send_message(
        message.chat.id,
        "Tilni tanlang / Choose language:",
        reply_markup=kb
    )

# Til tanlash
@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def set_language(call):
    lang = call.data.split("_")[1]
    user_lang[call.from_user.id] = lang

    bot.edit_message_text(
        "✅ Til tanlandi. Endi savol yozing.",
        call.message.chat.id,
        call.message.message_id
    )

# AI bilan suhbat
@bot.message_handler(func=lambda message: True)
def chat_ai(message):
    if message.from_user.id not in user_lang:
        bot.send_message(message.chat.id, "Avval /start bosing va til tanlang")
        return

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": message.text}
            ]
        )

        answer = response.choices[0].message.content
        bot.send_message(message.chat.id, answer)

    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik: {e}")

# Botni ishga tushirish
if __name__ == "__main__":
    bot.infinity_polling()
