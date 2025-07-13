import telebot
from telebot import types
from flask import Flask, request

TOKEN = '8147418547:AAEw9kZRAzpWEdbbwRSAphTvyCGH132gAOg'
CHANNEL_ID = '@bahanet1'
ADMIN_IDS = [2011180432, 6908531944]

WEBHOOK_URL = f'https://telebot-1-u1n4.onrender.com/{TOKEN}'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# بررسی عضویت
def is_user_member(user_id):
    try:
        member_status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return member_status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f'Error checking membership: {e}')
        return False


# خوش‌آمدگویی و بررسی عضویت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not is_user_member(message.chat.id):
        markup = types.InlineKeyboardMarkup()
        join_btn = types.InlineKeyboardButton("جوین شو 🔗", url="https://t.me/bahanet1")
        markup.add(join_btn)
        bot.send_message(message.chat.id, "👈 قبل از ادامه، باید عضو کانالمون باشی!", reply_markup=markup)
        return

    # فقط اگه عضو بود
    welcome_msg = "قراره تو عکس بفرستی، ما ذوق کنیم، بقیه رأی بدن، و یه نفر قهرمان شه! حالا نوبت توئه 🎯👑"
    bot.send_message(message.chat.id, welcome_msg)


# دریافت عکس
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if not is_user_member(message.chat.id):
        markup = types.InlineKeyboardMarkup()
        join_btn = types.InlineKeyboardButton("جوین شو 🔗", url="https://t.me/bahanet1")
        markup.add(join_btn)
        bot.send_message(message.chat.id, "👈 لطفاً اول عضو کانال شو بعد عکس بفرست 🙏", reply_markup=markup)
        return

    user = message.from_user
    first_name = user.first_name or "ندارد"
    last_name = user.last_name or "ندارد"
    username = f"@{user.username}" if user.username else "ندارد"
    user_id = user.id
    language = user.language_code or "نامشخص"
    profile_link = f"[لینک چت](tg://user?id={user_id})"

    user_info = (
        "📸 عکس جدید از کاربر\n\n"
        f"👤 نام: {first_name} {last_name}\n"
        f"🔗 یوزرنیم: {username}\n"
        f"🆔 آی‌دی عددی: `{user_id}`\n"
        f"🌐 زبان: {language}\n"
        f"🔗 پروفایل: {profile_link}"
    )

    for admin_id in ADMIN_IDS:
        # فوروارد خود عکس
        bot.forward_message(admin_id, message.chat.id, message.message_id)
        # ارسال اطلاعات کامل کاربر
        bot.send_message(admin_id, user_info, parse_mode="Markdown")

    # پیام تشکر به کاربر
    final_msg = "خیلی ممنونم بابت شرکت تو چالشمون 🙏🎉\nسلفی خوشگلت دریافت شد و بعد بررسی تو چنل قرار می‌گیره 📸\nو بعد رای‌گیری یه هدیه خیلی کوچیک از طرف ما قراره بگیری 🎁💝\nمنتظر خبرای خوب باش!"
    bot.send_message(message.chat.id, final_msg)


# وب‌هوک
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok'


# راه‌اندازی وب‌هوک
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host='0.0.0.0', port=5000)
