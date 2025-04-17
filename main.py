import requests
import time
import feedparser

# إعدادات البوت
BOT_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
SEND_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# روابط التغذية الإخبارية المراد متابعتها
RSS_FEEDS = [
    "https://beincrypto.com/feed/",  # المصدر الأساسي
    "https://cointelegraph.com/rss",
    "https://cryptopotato.com/feed"
]

# تخزين آخر عنوان تم إرساله لتجنب التكرار
latest_titles = []

def fetch_news():
    global latest_titles
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:  # نأخذ فقط آخر 5 أخبار من كل مصدر
            title = entry.title
            link = entry.link
            summary = entry.summary[:300]

            if title not in latest_titles:
                latest_titles.append(title)
                if len(latest_titles) > 50:
                    latest_titles = latest_titles[-50:]

                message = f"**خبر ترند جديد:**\n{title}\n\n{summary}\n\nرابط الخبر: {link}"
                send_message(message)

def send_message(text):
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(SEND_URL, json=payload)

# تكرار التحقق كل 5 دقائق
while True:
    try:
        fetch_news()
        time.sleep(300)
    except Exception as e:
        error_msg = f"حدث خطأ في البوت:\n{str(e)}"
        send_message(error_msg)
        time.sleep(60)
