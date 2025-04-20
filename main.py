import requests
import time

# بياناتك (استبدلها بالقيم الصحيحة فقط)
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "YOUR_CRYPTOPANIC_API_KEY"

# دوال الفلترة
def is_trending(news_item):
    return news_item.get("votes", {}).get("positive", 0) >= 20

def is_mining_related(text):
    keywords = ["mining", "hashrate", "asic", "antminer", "whatsminer"]
    return any(word in text.lower() for word in keywords)

def is_airdrop_related(text):
    keywords = ["airdrop", "claim", "snapshot", "retroactive", "free token"]
    return any(word in text.lower() for word in keywords)

def is_important(text):
    keywords = ["bitcoin", "ethereum", "binance", "sec", "etf", "coinbase", "blackrock"]
    return any(word in text.lower() for word in keywords)

# إرسال تيليجرام
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    print("Telegram Response:", response.status_code, response.text)

# جلب أخبار الكريبتو
def fetch_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&public=true"
    response = requests.get(url)

    if response.status_code != 200:
        print("فشل جلب الأخبار:", response.status_code)
        return

    news_items = response.json().get("results", [])
    sent_anything = False

    for item in news_items:
        title = item.get("title", "")
        link = item.get("url", "")

        if is_airdrop_related(title):
            msg = f"🔵 Airdrop:\n{title}\n{link}"
        elif is_mining_related(title):
            msg = f"⚒️ تعدين:\n{title}\n{link}"
        elif is_trending(item):
            msg = f"🔥 ترند:\n{title}\n{link}"
        elif is_important(title):
            msg = f"📌 خبر مهم:\n{title}\n{link}"
        else:
            continue

        send_to_telegram(msg)
        sent_anything = True

    if not sent_anything:
        send_to_telegram("✅ تم الفحص: لا يوجد خبر ينطبق عليه الفلاتر حالياً.")

# التشغيل
if __name__ == "__main__":
    fetch_crypto_news()
