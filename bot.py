from flask import Flask, request
import telebot
import time

API_TOKEN = '8147418547:AAEw9kZRAzpWEdbbwRSAphTvyCGH132gAOg'
bot = telebot.TeleBot(API_TOKEN)

WEBHOOK_URL = 'https://telebot-1-u1n4.onrender.com/'

app = Flask(__name__)

# تنظیم پیام شروع
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "قراره تو عکس بفرستی، ما ذوق کنیم، بقیه رأی بدن، و یه نفر قهرمان شه! حالا نوبت توئه 🎯👑")

# مسیر وبهوک
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid request', 403

# حذف و تنظیم مجدد وبهوک
bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url=WEBHOOK_URL)

# اجرای اپ
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
