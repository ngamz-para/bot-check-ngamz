import telebot
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN = "@Ngamz"
BOT_NAME = "BOT CHECK NGAMZ"

def get_fb_info(uid):
    url = f"https://www.facebook.com/profile.php?id={uid}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    name = "Không xác định"
    title = soup.find("title")
    if title:
        name = title.text.replace(" | Facebook", "")

    return {
        "name": name,
        "profile": url
    }

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
    f"""⚡️ {BOT_NAME}

👉 Gửi UID Facebook để check
👉 Chỉ dữ liệu công khai
👉 Không xâm phạm quyền riêng tư
""")

@bot.message_handler(func=lambda m: True)
def check(message):
    uid = message.text.strip()

    if not uid.isdigit():
        bot.reply_to(message, "❌ UID không hợp lệ")
        return

    info = get_fb_info(uid)
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    msg = f"""
🔍 FACEBOOK INFO | NGAMZ DEV

👤 Tên: {info['name']}
🆔 UID: {uid}
🔗 Profile: {info['profile']}

🌍 Locale: vi_VN 🇻🇳
🔐 Verified: Chưa xác minh
📅 Cập nhật: {now}

⚡ Admin: {ADMIN}
🟢 Trạng thái: Good
"""

    bot.reply_to(message, msg)

bot.infinity_polling()
