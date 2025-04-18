import requests
import time
from googletrans import Translator

# إعدادات
TELEGRAM_BOT_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
TELEGRAM_CHAT_ID = "-4734806120"
NEWSAPI_KEY = "af664841cdcd4c27a050b06660d1b2f0"

def translate_text(text):
    translator = Translator()
    try:
        result = translator.translate(text, dest='ar')
        return result.text
    except:
        return text

def fetch_trending_news():
    url = f"https://newsapi.org/v2/top-headlines?category=business&q=crypto&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "articles" in data and len(data["articles"]) > 0:
        article = data["articles"][0]
        title = article["title"]
        url = article["url"]

        # ترجمة العنوان مع استثناء الكلمات المهمة
        translated_title = translate_text(title)
        
        return f"خبر ترند حالياً:\n\n{translated_title}\n\nالمصدر: {url}"
    else:
        return None

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    requests.post(url, data=payload)

def main_loop():
    send_message("تم تشغيل السكربت")
    while True:
        try:
            news = fetch_trending_news()
            if news:
                send_message(news)
            else:
                send_message("تم الفحص ومافي خبر يستاهل")
        except Exception as e:
            send_message(f"حدث خطأ: {str(e)}")
        time.sleep(600)  # كل 10 دقائق

if __name__ == "__main__":
    main_loop()
