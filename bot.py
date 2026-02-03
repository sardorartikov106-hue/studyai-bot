import telebot
import os

# Tokenni Environment Variable orqali olish
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

LANGUAGES = ['O\'zbek', 'Русский', 'English']
FAN_PANEL = ['Matematika', 'Fizika', 'Kimyo', 'Biologiya', 'Tarix', 'Geografiya', 'Ingliz tili', 'Ona tili']
ADMIN_USER = '@S_28_08'

@bot.message_handler(commands=['start'])
def start(message):
    menu = "Tilni tanlang / Выберите язык / Select language:\n"
    for lang in LANGUAGES:
        menu += f' - {lang}\n'
    bot.reply_to(message, f"Salom! Men Sardor yaratgan StudyAi Assistantman.\n" + menu)

@bot.message_handler(func=lambda message: message.text in FAN_PANEL)
def fan_panel(message):
    bot.reply_to(message, f"Siz {message.text} fanini tanladingiz. Savolingizni yozing, AI javob beradi.")

@bot.message_handler(func=lambda message: message.text not in FAN_PANEL and message.text not in LANGUAGES)
def ai_reply(message):
    bot.reply_to(message, f"AI javob: Siz yozdingiz '{message.text}'")
    bot.send_message(ADMIN_USER, f"Foydalanuvchi {message.from_user.username} yozdi: {message.text}")

bot.polling()
