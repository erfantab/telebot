import telebot
from telebot import types
from flask import Flask, request

TOKEN = '8147418547:AAEw9kZRAzpWEdbbwRSAphTvyCGH132gAOg'
CHANNEL_ID = '@bahanet1'
ADMIN_IDS = [2011180432, 6908531944]

WEBHOOK_URL = f'https://telebot-1-u1n4.onrender.com/{TOKEN}'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# پیام خوش آمدگویی و چک عضویت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = "قراره تو عکس بفرستی، ما ذوق کنیم، بقیه رأی بدن، و یه نفر قهرمان شه! حالا نوبت توئه 🎯👑"
    bot.send_message(message.chat.id, welcome_msg)

    # چک عضویت
    try:
        user_status = bot.get_chat_member(CHANNEL_ID, message.chat.id).status
        if user_status not in ['member', 'creator', 'administrator']:
            markup = types.InlineKeyboardMarkup()
            join_btn = types.InlineKeyboardButton("جوین شو 🔗", url="https://t.me/bahanet1")
            markup.add(join_btn)
            bot.send_message(message.chat.id, "👈 قبل از ادامه، باید عضو کانالمون باشی!", reply_markup=markup)
    except Exception as e:
        print(f"Error checking membership: {e}")


# هندل عکس
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # ارسال به ادمین‌ها
        for admin_id in ADMIN_IDS:
            bot.forward_message(admin_id, message.chat.id, message.message_id)

        # پاسخ به کاربر
        final_msg = "خیلی ممنونم بابت شرکت تو چالشمون 🙏🎉\nسلفی خوشگلت دریافت شد و بعد بررسی تو چنل قرار می‌گیره 📸\nو بعد رای‌گیری یه هدیه خیلی کوچیک از طرف ما قراره بگیری 🎁💝\nمنتظر خبرای خوب باش!"
        bot.send_message(message.chat.id, final_msg)

    except Exception as e:
        print(f"Error forwarding photo: {e}")


# مسیر دریافت وب‌هوک
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok'


# راه‌اندازی سرور Flask
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host='0.0.0.0', port=5000)
