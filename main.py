import requests
import time

# إعدادات البوت
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "af664841cdcd4c27a050b06660d1b2f0"

# تصنيف مبسط للخبر
def classify_post(post):
    title = post.get("title", "").lower()
    if any(t in title for t in ["airdrop", "airdrops", "claim"]):
        return "Airdrop"
    if post.get("importance", 0) >= 3:
        return "مهم"
    if post.get("votes", {}).get("positive", 0) > 10:
        return "ترند"
    return "تجربة"

# تجهيز الرسالة
def prepare_message(post):
    title = post.get("title", "لا يوجد عنوان")
    url = post.get("url", "")
    classification = classify_post(post)

    print(f"[✓] عنوان الخبر: {title}")
    print(f"[✓] التصنيف: {classification}")

    message = f"#{classification}\n\n"
    message += f"**{title}**\n\n"
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
        print(f"[!] فشل إرسال الرسالة، كود الاستجابة: {response.status_code}, الرد: {response.text}")

# جلب الأخبار من CryptoPanic
def fetch_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&kind=news&public=true"
    response = requests.get(url)
    if response.status_code == 200:
        print("[✓] تم جلب الأخبار.")
        return response.json().get("results", [])
    print(f"[!] فشل جلب الأخبار: {response.status_code}")
    return []

# نقطة البداية
def main():
    posts = fetch_crypto_news()
    print(f"[✓] عدد الأخبار: {len(posts)}")
    for post in posts[:3]:  # نرسل فقط أول 3 أخبار لتجربة أسرع
        msg = prepare_message(post)
        send_telegram_message(msg)
        time.sleep(2)

if __name__ == "__main__":
    main()
