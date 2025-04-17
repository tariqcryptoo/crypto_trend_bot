import time
import requests
import telegram
from bs4 import BeautifulSoup

TOKEN = '7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ'
CHAT_ID = -4734806120
bot = telegram.Bot(token=TOKEN)

def fetch_trending_news():
    try:
        url = 'https://beincrypto.com/news/'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')

        trending = []
        for article in articles:
            title_tag = article.find('h3')
            if title_tag:
                title = title_tag.text.strip()
                link = article.find('a', href=True)['href']
                if "bitcoin" in title.lower() or "crypto" in title.lower():
                    trending.append(f"{title}\n{link}")
        return trending
    except Exception as e:
        return f"Error while fetching news: {e}"

while True:
    try:
        bot.send_message(chat_id=CHAT_ID, text="تم تشغيل السكربت")

        trending_news = fetch_trending_news()

        if isinstance(trending_news, str):
            # رسالة الخطأ
            bot.send_message(chat_id=CHAT_ID, text=trending_news)
        elif trending_news:
            for news in trending_news[:3]:  # نرسل فقط أول 3 أخبار ترند
                bot.send_message(chat_id=CHAT_ID, text=news)
        else:
            bot.send_message(chat_id=CHAT_ID, text="تم الفحص ومافي خبر يستاهل")
    except Exception as error:
        bot.send_message(chat_id=CHAT_ID, text=f"خطأ في التشغيل: {error}")

    time.sleep(600)  # كل 10 دقائق
