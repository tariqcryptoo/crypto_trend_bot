import requests
import time
from deep_translator import GoogleTranslator
import html
import re

# إعدادات البوت
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "af664841cdcd4c27a050b06660d1b2f0"

# الترجمة الذكية
def translate_text(text):
    try:
        return GoogleTranslator(source='auto', target='ar').translate(text)
    except Exception as e:
        print(f"[!] فشل في الترجمة: {e}")
        return "تعذر ترجمة النص."

# تنظيف HTML من النص
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return html.unescape(cleantext)

# تصنيف الخبر
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

    if not classification:
        classification = "تجربة"

    print(f"[✓] الخبر: {title}")
    print(f"[✓] التصنيف: {classification}")
    print(f"[✓] الترجمة: {translated[:60]}...")

    message = f"#{classification}\n\n"
    message += f"**{title}**\n\n"
    message += f"{translated}\n\n"
    message += f"رابط الخبر: {url}"
    return message

# إرسال الرسالة إلى تيليجرام
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("[✓] تم إرسال الرسالة لتليجرام.")
    else:
        print(f"[!] فشل إرسال الرسالة، الكود: {response.status_code}, الرد: {response.text}")
    return response.status_code == 200

# جلب الأخبار من CryptoPanic
def fetch_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&kind=news&public=true"
    response = requests.get(url)
    if response.status_code == 200:
        print("[✓] تم جلب الأخبار بنجاح.")
        return response.json().get("results", [])
    print(f"[!] فشل في جلب الأخبار: {response.status_code}")
    return []

# نقطة البداية
def main():
    posts = fetch_crypto_news()
    print(f"[✓] عدد الأخبار المستلمة: {len(posts)}")
    for post in posts:
        msg = prepare_message(post)
        if msg:
            send_telegram_message(msg)
            time.sleep(2)

if __name__ == "__main__":
    main()
