import requests
from deep_translator import GoogleTranslator

TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "9889e4a8021167e15bc0d74858809a6e0195fa2e"

# إعادة صياغة الخبر بلغة بشرية مبسطة
def human_rewrite(title):
    title = title.lower()
    if "airdrop" in title:
        return "تم الإعلان عن توزيع مجاني (Airdrop) جديد."
    if "binance" in title and "support" in title:
        return "منصة Binance أعلنت دعمًا جديدًا لعملة رقمية."
    if "whale" in title and "sell" in title:
        return "حوت كريبتو قام ببيع ضخم قد يؤثر على السوق."
    if "mining" in title or "hashrate" in title or "asic" in title:
        return "تحديث جديد في مجال التعدين أو زيادة في hashrate."
    if "etf" in title or "sec" in title:
        return "تحديث متعلق بصناديق ETF أو تنظيمات هيئة SEC."
    if "launch" in title or "mainnet" in title or "testnet" in title:
        return "إطلاق شبكة أو مشروع جديد في السوق."
    if "exploit" in title or "hack" in title:
        return "تحذير: تم رصد اختراق أو ثغرة في مشروع كريبتو."
    if "investment" in title or "funding" in title:
        return "خبر عن استثمار أو تمويل كبير لمشروع جديد."
    return None

# إرسال الرسالة إلى تلغرام
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

# جلب الأخبار وتحليلها
def fetch_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&public=true"
    try:
        res = requests.get(url)
        news = res.json().get("results", [])
    except:
        send_to_telegram("❌ خطأ في الاتصال بمصدر الأخبار.")
        return

    count = 0
    for item in news:
        if count >= 3:
            break

        title_en = item.get("title", "")
        link = item.get("url", "")
        summary = human_rewrite(title_en)

        if summary:
            try:
                translated_title = GoogleTranslator(source='en', target='ar').translate(title_en)
                message = f"*{summary}*\n\nالعنوان: {translated_title}\n{link}"
                send_to_telegram(message)
                count += 1
            except:
                continue

    if count == 0:
        send_to_telegram("✅ تم الفحص: لا يوجد خبر واضح ومفهوم حاليًا.")

# تشغيل البوت
if __name__ == "__main__":
    fetch_crypto_news()
