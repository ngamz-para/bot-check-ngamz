import os
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

# ===== ƯỚC LƯỢNG =====
def estimate_created_year(uid: int):
    if uid < 10**14:
        return "2015–2017", "7–9 năm"
    elif uid < 3*10**14:
        return "2018–2020", "4–6 năm"
    elif uid < 5*10**14:
        return "2021–2022", "2–3 năm"
    elif uid < 7*10**14:
        return "2023", "1–2 năm"
    else:
        return "2024–2025", "< 1 năm"

def estimate_followers(uid: int):
    if uid < 3*10**14:
        return random.randint(500, 5000)
    elif uid < 6*10**14:
        return random.randint(100, 3000)
    else:
        return random.randint(0, 800)

def estimate_friends(uid: int):
    if uid < 3*10**14:
        return random.randint(500, 3000)
    elif uid < 6*10**14:
        return random.randint(200, 1500)
    else:
        return random.randint(50, 800)

# ===== LẤY INFO PUBLIC =====
def get_fb_public(uid: str):
    url = f"https://graph.facebook.com/{uid}?fields=id,name,gender,locale,link&access_token=123"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return {}

# ===== XỬ LÝ MESSAGE =====
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("❌ Vui lòng nhập UID Facebook (chỉ số).")
        return

    uid = int(text)
    data = get_fb_public(text)

    name = data.get("name", "Không xác định")
    gender = data.get("gender", "Ẩn")
    locale = data.get("locale", "Không xác định")
    link = data.get("link", f"https://www.facebook.com/profile.php?id={text}")

    year_est, age_est = estimate_created_year(uid)
    followers = estimate_followers(uid)
    friends = estimate_friends(uid)

    msg = f"""
👤 Tên: {name}
🆔 UID: {text}
🧷 Username: Không có username
✅ Verified: Chưa xác minh 🔴
📅 Đăng ký: {year_est}
🧮 Tuổi tài khoản: {age_est}
━━━━━━━━━━━━━━━━━━━━━━
🚻 Giới tính: {gender}
❤️ Quan hệ: Không có dữ liệu!
🏡 Quê quán: Ẩn
📍 Đang sống: Ẩn
━━━━━━━━━━━━━━━━━━━━━━
🌐 Locale: {locale}
🌎 Quốc gia: Vietnam 🇻🇳
🔗 Profile: {link}
👥 Follower: ~{followers}
👤 Bạn bè: ~{friends}
━━━━━━━━━━━━━━━━━━━━━━
⚡️ Admin: @YourName | Trạng thái: Good 🟢
📦 BOT CHECK NGAMZ
    """

    await update.message.reply_text(msg)

# ===== MAIN =====
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()
