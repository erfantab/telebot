import telebot
from telebot import types
from flask import Flask, request

app = Flask(__name__)

# توکن ربات
API_TOKEN = '8147418547:AAEw9kZRAzpWEdbbwRSAphTvyCGH132gAOg'
bot = telebot.TeleBot(API_TOKEN)

# آدرس وب‌هوک (URL) رندر شما
WEBHOOK_URL = 'https://telebot-1-u1n4.onrender.com/'  # تغییر به آدرس رندر شما

# تابع ارسال پیام خوشامدگویی
def send_welcome_message(chat_id):
    # ارسال پیام خوشامدگویی
    bot.send_message(chat_id, 
                     "قراره تو عکس بفرستی، ما ذوق کنیم، بقیه رأی بدن، و یه نفر قهرمان شه! حالا نوبت توئه 🎯👑")
    
    # ایجاد دکمه‌های جوین
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("جوین شو", url="https://t.me/bahanet1")  # لینک کانال شما
    markup.add(button)
    
    # ارسال دکمه جوین پس از پیام خوشامدگویی
    bot.send_message(chat_id, 
                     "برای شروع، لطفاً به کانال ما بپیوندید.",
                     reply_markup=markup)  # دکمه در پایین پیام

# هنگامی که کاربر استارت می‌کنه
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    send_welcome_message(chat_id)

# دریافت عکس از کاربر و ارسال به ادمین‌ها
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    # ارسال عکس به ادمین‌ها
    admin_ids = [2011180432, 6908531944]  # آی‌دی ادمین‌ها
    for admin_id in admin_ids:
        bot.send_photo(admin_id, file_path)

    # تایید دریافت عکس به کاربر
    bot.send_message(chat_id, 
                     "خیلی ممنونم بابت شرکت تو چالشمون! 😊 سلفی خوشگلت دریافت شد 📸 و بعد از بررسی تو چنل قرار می‌گیره. پس از رای‌گیری، یه هدیه خیلی کوچیک از طرف ما قراره بگیری 🎁✨\n\nمنتظر خبرای خوب باش! 🌟")

# وب‌هوک رو تنظیم کن
@app.route('/' + API_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

# تابع برای راه‌اندازی وب‌هوک
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + API_TOKEN)

# راه‌اندازی وب‌هوک در ابتدا
set_webhook()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
