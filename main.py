import requests
import time
from deep_translator import GoogleTranslator
import html
import re

# إعدادات البوت
TELEGRAM_TOKEN = "توكن_البوت"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "مفتاح_CryptoPanic"

# الترجمة الذكية
def translate_text(text):
    return GoogleTranslator(source='auto', target='ar').translate(text)

# فلترة HTML
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return html.unescape(cleantext)

# تحديد نوع الخبر
def classify_post(post):
    title = post.get("title", "").lower()
    tags = post.get("tags", [])
    if any(t in title for t in ["airdrop", "airdrops", "claim"]):
        return "Airdrop"
    if "important" in tags or post.get("importance", 0) >= 3:
        return "مهم"
    if post.get("votes", {}).get("positive", 0) > 10:
        return "ترند"
    return None

# تجهيز الرسالة
def prepare_message(post):
    title = post.get("title", "لا يوجد عنوان")
    content = post.get("content") or post.get("description") or title
    url = post.get("url", "")
    translated = translate_text(clean_html(content))
    classification = classify_post(post)

    # أثناء الاختبار: لو ما فيه تصنيف، نعتبره "تجربة"
    if not classification:
        classification = "تجربة"

    message = f"#{classification}\n\n"
    message += f"**{title}**\n\n"
    message += f"{translated}\n\n"
    message += f"رابط الخبر: {url}"
    return message

# إرسال لتليجرام
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    return response.status_code == 200

# جلب الأخبار
def fetch_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&kind=news&public=true"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

# نقطة البداية
def main():
    posts = fetch_crypto_news()
    for post in posts:
        msg = prepare_message(post)
        if msg:
            send_telegram_message(msg)
            time.sleep(2)  # تأخير لتفادي حظر تيليجرام

if __name__ == "__main__":
    main()
