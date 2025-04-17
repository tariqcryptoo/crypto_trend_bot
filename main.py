import logging
import requests
import time
from telegram import Bot
from telegram.constants import ParseMode
from deep_translator import GoogleTranslator

# بيانات التوكن ومعرف القروب
BOT_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
GROUP_ID = -4734806120

# إعداد البوت
bot = Bot(token=BOT_TOKEN)

# إعدادات السجل
logging.basicConfig(level=logging.INFO)

def translate_text(text):
    # كلمات ما نترجمها
    exclude = ['Bitcoin', 'Ethereum', 'Binance', 'NFT', 'DeFi', 'Web3', 'Solana', 'Coinbase']
    for word in exclude:
        text = text.replace(word, f'[[[{word}]]]')
    translated = GoogleTranslator(source='auto', target='ar').translate(text)
    for word in exclude:
        translated = translated.replace(f'[[[{word}]]]', word)
    return translated

def fetch_news():
    url = "https://cryptopanic.com/api/v1/posts/?auth_token=8e49fffbeb8b7f25cc3caa60c1d4c868b6fc30a7&public=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        posts = data.get("results", [])
        if posts:
            return posts
    return []

def is_trending(post):
    votes = post.get('votes', {})
    return votes.get('positive', 0) >= 2 or votes.get('important', 0) >= 1

def main():
    sent_urls = set()
    bot.send_message(chat_id=GROUP_ID, text="تم تشغيل السكربت")
    while True:
        try:
            news = fetch_news()
            sent = False
            for post in news:
                url = post.get("url")
                if url not in sent_urls and is_trending(post):
                    title = post.get("title")
                    translated_title = translate_text(title)
                    message = f"*خبر ترند جديد:*\n\n{translated_title}\n\n[رابط الخبر]({url})"
                    bot.send_message(chat_id=GROUP_ID, text=message, parse_mode=ParseMode.MARKDOWN)
                    sent_urls.add(url)
                    sent = True
            if not sent:
                bot.send_message(chat_id=GROUP_ID, text="تم الفحص ومافي خبر يستاهل")
        except Exception as e:
            logging.error(f"Error occurred: {e}")
        time.sleep(600)  # كل 10 دقايق

if __name__ == "__main__":
    main()
