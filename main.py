import requests
import time
from googletrans import Translator

TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
CRYPTO_API_KEY = "YOUR_CRYPTOPANIC_API_KEY"

translator = Translator()

def translate_text(text):
    result = translator.translate(text, src='en', dest='ar')
    return result.text

def is_trending(news_item):
    return news_item.get("votes", {}).get("positive", 0) >= 20

def is_mining_related(text):
    mining_keywords = ["mining", "hashrate", "ASIC", "Antminer", "Whatsminer", "Ethereum mining"]
    return any(keyword.lower() in text.lower() for keyword in mining_keywords)

def is_airdrop_related(text):
    airdrop_keywords = ["airdrop", "claim", "snapshot", "retroactive", "free token"]
    return any(keyword.lower() in text.lower() for keyword in airdrop_keywords)

def is_important(text):
    important_keywords = ["bitcoin", "ethereum", "binance", "SEC", "ETF", "blackrock", "coinbase", "spot trading"]
    return any(keyword.lower() in text.lower() for keyword in important_keywords)

def fetch_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&public=true"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching data:", response.status_code)
        return

    news_items = response.json().get("results", [])
    for item in news_items:
        title = item.get("title", "")
        url = item.get("url", "")
        translated = translate_text(title)

        if is_airdrop_related(title):
            message = f"🔵 تصنيف: Airdrop\n{translated}\n{url}"
        elif is_mining_related(title):
            message = f"⚒️ تصنيف: تعدين مهم جدًا\n{translated}\n{url}"
        elif is_trending(item):
            message = f"🔥 تصنيف: ترند\n{translated}\n{url}"
        elif is_important(title):
            message = f"📌 تصنيف: خبر مهم\n{translated}\n{url}"
        else:
            continue  # تجاهل الأخبار اللي مو ضمن المعايير

        send_to_telegram(message)

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("فشل إرسال الخبر للتليجرام:", response.status_code)

if __name__ == "__main__":
    while True:
        fetch_crypto_news()
        time.sleep(600)  # كل 10 دقائق
