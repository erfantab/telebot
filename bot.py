
import telebot

TOKEN = "8147418547:AAEw9kZRAzpWEdbbwRSAphTvyCGH132gAOg"
bot = telebot.TeleBot(TOKEN)

# لیست آی‌دی عددی ادمین‌ها
ADMIN_IDS = [2011180432, 6908531944]

# یوزرنیم کانال برای بررسی عضویت
CHANNEL_USERNAME = '@bahanet1'

# چک می‌کنه کاربر عضو کانال هست یا نه
def is_user_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

# پیام /start با چک کردن عضویت
@bot.message_handler(commands=['start'])
def start(message):
    if not is_user_member(message.from_user.id):
        bot.send_message(message.chat.id, f"برای استفاده از ربات، اول باید عضو کانال {CHANNEL_USERNAME} بشی 🌟")
        return
    bot.send_message(message.chat.id, "قراره تو عکس بفرستی، ما ذوق کنیم، بقیه رأی بدن، و یه نفر قهرمان شه! حالا نوبت توئه 🎯👑")

# دریافت و فوروارد عکس‌ها به ادمین‌ها
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    for admin_id in ADMIN_IDS:
        try:
            bot.forward_message(chat_id=admin_id, from_chat_id=message.chat.id, message_id=message.message_id)
        except Exception as e:
            print(f"Error sending to admin {admin_id}: {e}")
    bot.reply_to(message, "عکست دریافت شد! منتظر رأی‌ها باش! 🔥📸")

# اجرای ربات با webhook
import flask
from flask import request

WEBHOOK_URL = 'https://telebot-1-u1n4.onrender.com/'  # آدرس دامنه رندر
WEBHOOK_PATH = f"/{TOKEN}/"
WEBHOOK_LISTEN = "0.0.0.0"
WEBHOOK_PORT = 10000

app = flask.Flask(__name__)

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

import os
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + TOKEN + '/')
    app.run(host=WEBHOOK_LISTEN, port=int(os.environ.get('PORT', WEBHOOK_PORT)))
