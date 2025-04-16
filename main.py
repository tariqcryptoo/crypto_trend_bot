
import requests
import time
import telegram
from bs4 import BeautifulSoup

# إعدادات البوت
BOT_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = None

bot = telegram.Bot(token=BOT_TOKEN)

def get_trending_news():
    url = "https://beincrypto.com/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    headlines = soup.select("h3 a")[:3]  # أول 3 عناوين
    news_list = []

    for item in headlines:
        title = item.get_text(strip=True)
        link = item['href']
        if not link.startswith("http"):
            link = "https://beincrypto.com" + link
        news_list.append((title, link))

    return news_list

def send_news(news):
    global CHAT_ID
    updates = bot.get_updates()
    if updates:
        CHAT_ID = updates[-1].message.chat.id
    else:
        return

    for title, link in news:
        message = f"🔥 ترند كريبتو جديد:\n\n📌 {title}\n🔗 {link}"
        bot.send_message(chat_id=CHAT_ID, text=message)
        time.sleep(2)

if __name__ == "__main__":
    trending_news = get_trending_news()
    send_news(trending_news)
