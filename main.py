import requests
import time
from deep_translator import GoogleTranslator
from telegram import Bot

# إعدادات الاتصال
BOT_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = -4734806120
NEWS_API_KEY = "af664841cdcd4c27a050b06660d1b2f0"

bot = Bot(token=BOT_TOKEN)

# كلمات لا تترجم
EXCLUDE = ['Bitcoin', 'Ethereum', 'Solana', 'Binance', 'SEC', 'ETF', 'airdrop', 'Crypto', 'DeFi', 'Web3', 'Ripple', 'USDT', 'USDC']

# كلمات تدل على خبر ترند قوي
TREND_KEYWORDS = ['hack', 'etf', 'arrest', 'scam', 'exploit', 'rug pull', 'pump', 'dump', 'collapse', 'crash', 'lawsuit']

# كلمات تدل على أخبار مهمة
IMPORTANT_KEYWORDS = ['update', 'launch', 'support', 'network', 'integrate', 'partnership', 'statement', 'feature']

def translate_smart(text):
    for word in EXCLUDE:
        text = text.replace(word, f'[[[{word}]]]')
    translated = GoogleTranslator(source='auto', target='ar').translate(text)
    for word in EXCLUDE:
        translated = translated.replace(f'[[[{word}]]]', word)
    return translated

def fetch_news():
    url = f"https://newsapi.org/v2/everything?q=crypto&language=en&apiKey={NEWS_API_KEY}&pageSize=10"
    response = requests.get(url)
    return response.json().get("articles", [])

def classify_and_send():
    articles = fetch_news()
    sent = False

    # أخبار ترند قوية
    for article in articles:
        title = article.get("title", "")
        url = article.get("url", "")
        title_lower = title.lower()

        if any(word in title_lower for word in TREND_KEYWORDS):
            translated = translate_smart(title)
            message = f"🔥 *خبر ترند:*\n{translated}\n[رابط الخبر]({url})"
            bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
            sent = True
            break

    # أخبار مهمة
    for article in articles:
        title = article.get("title", "")
        url = article.get("url", "")
        title_lower = title.lower()

        if any(word in title_lower for word in IMPORTANT_KEYWORDS):
            translated = translate_smart(title)
            message = f"ℹ️ *خبر مهم:*\n{translated}\n[رابط الخبر]({url})"
            bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
            sent = True
            break

    if not sent:
        bot.send_message(chat_id=CHAT_ID, text="✅ تم الفحص ومافي أخبار بارزة حاليًا.")

# بداية التشغيل
bot.send_message(chat_id=CHAT_ID, text="✅ تم تشغيل السكربت - نتابع الأخبار كل 10 دقايق")

while True:
    try:
        classify_and_send()
    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text=f"❌ خطأ: {str(e)}")
    time.sleep(600)
