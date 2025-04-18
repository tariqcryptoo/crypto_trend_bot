import requests
from telegram import Bot
from deep_translator import GoogleTranslator

BOT_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = -4734806120
NEWS_API_KEY = "af664841cdcd4c27a050b06660d1b2f0"

bot = Bot(token=BOT_TOKEN)

EXCLUDE = ['Bitcoin', 'Ethereum', 'Solana', 'Binance', 'SEC', 'ETF', 'airdrop', 'Crypto', 'DeFi']

def translate_smart(text):
    try:
        for word in EXCLUDE:
            text = text.replace(word, f'[[[{word}]]]')
        translated = GoogleTranslator(source='auto', target='ar').translate(text)
        for word in EXCLUDE:
            translated = translated.replace(f'[[[{word}]]]', word)
        return translated
    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text=f"⚠️ خطأ في الترجمة: {e}")
        return text

def fetch_and_send_news():
    bot.send_message(chat_id=CHAT_ID, text="✅ بدأ فحص NewsAPI...")

    try:
        url = f"https://newsapi.org/v2/everything?q=bitcoin OR crypto&language=en&pageSize=1&apiKey={NEWS_API_KEY}"
        res = requests.get(url)
        data = res.json()

        if "articles" in data and len(data["articles"]) > 0:
            article = data["articles"][0]
            title = article.get("title", "")
            link = article.get("url", "")

            translated = translate_smart(title)
            message = f"*عنوان:* {translated}\n[رابط الخبر]({link})"
            bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        else:
            bot.send_message(chat_id=CHAT_ID, text="✅ الاتصال شغال لكن مافي أخبار ترند حالياً.")

    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text=f"❌ خطأ في الاتصال بـ NewsAPI:\n{e}")

# تنفيذ مباشر لمرة واحدة
fetch_and_send_news()
