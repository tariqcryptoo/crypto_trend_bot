import requests
import time
import telegram
from googletrans import Translator

# بيانات البوت
BOT_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = -4734806120
API_KEY = "cp_5df7eaf3b2f5a0e58074b9f8b9aa2687"  # CryptoPanic API

bot = telegram.Bot(token=BOT_TOKEN)
translator = Translator()

# مصطلحات ما نترجمها
preserve_terms = ['Bitcoin', 'Ethereum', 'Solana', 'Binance', 'SEC', 'ETF', 'airdrop', 'bullish', 'bearish', 'Rug Pull', 'Crypto', 'DeFi']

def translate_smart(text):
    for term in preserve_terms:
        text = text.replace(term, f"@@{term}@@")
    translated = translator.translate(text, dest='ar').text
    for term in preserve_terms:
        translated = translated.replace(f"@@{term}@@", term)
    return translated

def get_trending_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={API_KEY}&filter=important,bullish"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    articles = data.get("results", [])
    trending = []

    for article in articles:
        title = article.get("title", "")
        url = article.get("url", "")
        translated_title = translate_smart(title)
        full_msg = f"*عنوان:* {translated_title}\n[رابط الخبر]({url})"
        trending.append(full_msg)

    return trending

while True:
    try:
        trending_news = get_trending_news()

        if trending_news:
            for news in trending_news[:3]:
                bot.send_message(chat_id=CHAT_ID, text=news, parse_mode="Markdown", disable_web_page_preview=False)
        else:
            bot.send_message(chat_id=CHAT_ID, text="✅ تم الفحص ومافي خبر يستاهل.")
    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text=f"⚠️ حدث خطأ في البوت:\n{str(e)}")

    time.sleep(600)  # كل 10 دقائق
