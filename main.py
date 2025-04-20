import requests
import time

# بياناتك
TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
CRYPTO_API_KEY = "YOUR_CRYPTOPANIC_API_KEY"

# الفلاتر
def is_trending(news_item):
    return news_item.get("votes", {}).get("positive", 0) >= 20

def is_mining_related(text):
    mining_keywords = ["mining", "hashrate", "asic", "antminer", "whatsminer"]
    return any(word in text.lower() for word in mining_keywords)

def is_airdrop_related(text):
    airdrop_keywords = ["airdrop", "claim", "snapshot", "retroactive", "free token"]
    return any(word in text.lower() for word in airdrop_keywords)

def is_important(text):
    important_keywords = ["bitcoin", "ethereum", "binance", "sec", "etf", "coinbase", "blackrock"]
    return any(word in text.lower() for word in important_keywords)

# إرسال تيليجرام
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("فشل الإرسال:", response.status_code)

# جلب الأخبار
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

    # رسالة تأكيد حتى لو ما فيه شي مهم
    if not sent_anything:
        send_to_telegram("✅ تم الفحص: لا يوجد خبر ينطبق عليه الفلاتر حالياً.")

# التشغيل
if __name__ == "__main__":
    fetch_crypto_news()
