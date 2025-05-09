import telebot
from flask import Flask, request

# توکن ربات شما
TOKEN = '8147418547:AAEw9kZRAzpWEdbbwRSAphTvyCGH132gAOg'
# آیدی کانال شما
CHANNEL_ID = '@bahanet1'  
bot = telebot.TeleBot(TOKEN)

# ساخت یک اپلیکیشن Flask
app = Flask(__name__)

# دستور /start برای ربات
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    # چک کردن عضویت در کانال
    member = bot.get_chat_member(CHANNEL_ID, user_id)
    if member.status == 'member' or member.status == 'administrator':
        bot.send_message(user_id, "قراره تو عکس بفرستی، ما ذوق کنیم، بقیه رأی بدن، و یه نفر قهرمان شه! حالا نوبت توئه 🎯👑")
    else:
        bot.send_message(user_id, f"برای شرکت در مسابقه باید به کانال {CHANNEL_ID} عضو شوید.")

# برای دریافت پیام‌ها از تلگرام
@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

# تنظیم webhook برای ربات
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://your-render-url/' + TOKEN)  # آدرس رندر خود را جایگزین کنید
    app.run(host="0.0.0.0", port=5000)
