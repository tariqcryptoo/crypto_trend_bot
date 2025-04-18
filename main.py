import requests
import time
from telegram import Bot
from deep_translator import GoogleTranslator

# بيانات البوت والتليجرام
BOT_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
GROUP_ID = -4734806120

# مفتاح NewsAPI
NEWS_API_KEY = "af664841cdcd4c27a050b06660d1b2f0"
NEWS_API_URL = "https://newsapi.org/v2/everything"

# كلمات البحث المهمة
KEYWORDS = ["bitcoin", "crypto", "ethereum", "airdrop", "binance", "solana", "etf"]

# كلمات لا تترجم
EXCLUDE_TERMS = ['Bitcoin', 'Ethereum', 'Binance', 'NFT', 'DeFi', 'Web3', 'Solana', 'Coinbase', 'airdrop', 'ETF', 'SEC', 'Crypto']

# إعداد البوت
bot = Bot(token=BOT_TOKEN)

def translate_smart(text):
    for word in EXCLUDE_TERMS:
        text = text.replace(word, f'[[[{word}]]]')
    translated = GoogleTranslator(source='auto', target='ar').translate(text)
    for word in EXCLUDE_TERMS:
        translated = translated.replace(f'[[[{word}]]]', word)
    return translated

def fetch_news():
    params = {
        'q': ' OR '.join(KEYWORDS),
        'language': 'en',
        'sortBy': 'publishedAt',
        'apiKey': NEWS_API_KEY,
        'pageSize': 5,
    }
    response = requests.get(NEWS_API_URL, params=params)
    data = response.json()
    return data.get('articles', [])

sent_urls = set()

def main():
    bot.send_message(chat_id=GROUP_ID, text="تم تشغيل السكربت - فحص الأخبار كل 10 دقايق")

    while True:
        try:
            articles = fetch_news()
            sent = False
            for article in articles:
                url = article.get('url')
                if url in sent_urls:
                    continue

                title = article.get('title', '')
                if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
                    translated_title = translate_smart(title)
                    message = f"*خبر ترند جديد:*\n\n{translated_title}\n\n[رابط الخبر]({url})"
                    bot.send_message(chat_id=GROUP_ID, text=message, parse_mode="Markdown")
                    sent_urls.add(url)
                    sent = True
            if not sent:
                bot.send_message(chat_id=GROUP_ID, text="✅ تم الفحص ومافي خبر يستاهل.")
        except Exception as e:
            bot.send_message(chat_id=GROUP_ID, text=f"⚠️ خطأ: {str(e)}")

        time.sleep(600)  # كل 10 دقايق

if __name__ == "__main__":
    main()
