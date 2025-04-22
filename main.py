import requests
import time
import html

# إعدادات البوت
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "af664841cdcd4c27a050b06660d1b2f0"

# تصنيف ذكي للخبر
def classify_post(post):
    title = post.get("title", "").lower()
    importance = post.get("importance", 0)
    votes = post.get("votes", {}).get("positive", 0)

    if any(word in title for word in ["airdrop", "claim", "snapshot"]):
        return "Airdrop"
    if any(word in title for word in ["price analysis", "price prediction", "btc analysis", "eth analysis"]):
        return "تحليل سعر"
    if any(word in title for word in ["partnership", "collaborates", "joins forces", "integrates"]):
        return "شراكة"
    if any(word in title for word in ["launch", "mainnet", "testnet", "introduces", "unveils"]):
        return "مشروع جديد"
    if any(word in title for word in ["hack", "exploit", "rugpull", "scam", "security breach"]):
        return "تحذير"
    if any(word in title for word in ["funding", "raises", "investment", "vc", "backed"]):
        return "تمويل"
    if importance >= 3 or votes > 10:
        return "مهم / ترند"
    return "تجربة"

# تجهيز الرسالة
def prepare_message(post):
    title = html.escape(post.get("title", "لا يوجد عنوان"))
    url = html.escape(post.get("url", ""))
    classification = html.escape(classify_post(post)).replace("#", "&#35;")

    print("---")
    print(f"[خبر] العنوان: {title}")
    print(f"[خبر] التصنيف: {classification}")
    print(f"[خبر] الرابط: {url}")

    message = f"<b>{classification}</b>\n\n"
    message += f"<b>{title}</b>\n\n"
    message += f"<a href='{url}'>رابط الخبر</a>"
    return message

# إرسال الرسالة إلى تيليجرام
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("[✓] تم إرسال الرسالة لتليجرام.")
    else:
        print(f"[!] فشل إرسال الرسالة. كود: {response.status_code}, رد: {response.text}")

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
    print("[تشغيل] بدأ البوت الآن...")
    posts = fetch_crypto_news()
    print(f"[تشغيل] عدد الأخبار المستلمة: {len(posts)}")

    if not posts:
        print("[!] لا توجد أخبار حالياً.")
    else:
        for post in posts[:3]:
            try:
                msg = prepare_message(post)
                send_telegram_message(msg)
                time.sleep(2)
            except Exception as e:
                print(f"[!] خطأ أثناء المعالجة: {e}")

if __name__ == "__main__":
    main()
