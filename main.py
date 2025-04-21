import asyncio
import requests
from telegram import Bot
from deep_translator import GoogleTranslator

# بيانات التوكن والقروب
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"

bot = Bot(token=TELEGRAM_TOKEN)

# ترجمة + إعادة صياغة بشرية
def humanize_text(text):
    try:
        translated = GoogleTranslator(source='auto', target='ar').translate(text)
        if len(translated) > 400:
            return translated[:400] + "..."
        return translated
    except Exception as e:
        return "لم نستطع ترجمة الخبر حالياً."

# جلب الأخبار من CryptoPanic
def fetch_crypto_news():
    url = "https://cryptopanic.com/api/v1/posts/?auth_token=9889e4a8021167e15bc0d74858809a6e0195fa2e&filter=hot"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["results"]
    else:
        return []

# تجهيز الرسالة
def prepare_message(post):
    title = post["title"]
    link = post["url"]
    source = post["domain"]
    summary = humanize_text(post["content"] or post["title"])
    message = f"""عنوان مثير للاهتمام في سوق الكريبتو،
{summary}
المصدر: {source}
التفاصيل في الخبر:
{link}"""
    return message

# إرسال الرسائل
async def main():
    posts = fetch_crypto_news()
    if not posts:
        await bot.send_message(chat_id=CHAT_ID, text="ما في أخبار حالياً.")
        return

    for post in posts[:3]:  # نرسل أول 3 فقط عشان ما نزعج التيليجرام
        msg = prepare_message(post)
        await bot.send_message(chat_id=CHAT_ID, text=msg)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
