import requests

# إعدادات البوت
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "9889e4a8021167e15bc0d74858809a6e0195fa2e"

# إعادة الصياغة البشرية
def rewrite_human_friendly(title):
    if not title:
        return None

    title_lower = title.lower()

    if "airdrop" in title_lower:
        return "تم الإعلان عن Airdrop جديد، تابع التفاصيل."
    elif "binance" in title_lower and "support" in title_lower:
        return "منصة Binance أعلنت دعمًا لعملة جديدة."
    elif "whale" in title_lower and "sell" in title_lower:
        return "حوت كريبتو قام ببيع كبير، قد يؤثر على السوق."
    elif "launch" in title_lower or "released" in title_lower:
        return "إطلاق رسمي لمشروع أو منتج جديد."
    elif "testnet" in title_lower or "mainnet" in title_lower:
        return "إطلاق شبكة اختبارية أو رئيسية لمشروع كريبتو."
    elif "etf" in title_lower or "sec" in title_lower:
        return "تحديث تنظيمي أو خبر متعلق بصناديق ETF."
    elif "partnership" in title_lower or "collaborat" in title_lower:
        return "شراكة جديدة بين جهات في عالم الكريبتو."
    elif "hack" in title_lower or "exploit" in title_lower:
        return "تحذير: تم اكتشاف اختراق أو ثغرة أمنية."
    elif "btc" in title_lower and "recovery" in title_lower:
        return "البيتكوين يشهد تعافي وارتفاع في السعر."
    elif "investment" in title_lower or "funding" in title_lower:
        return "خبر عن تمويل جديد أو استثمار كبير."
    elif "stablecoin" in title_lower:
        return "زيادة الاهتمام بعملات الـStablecoin في الأسواق."
    elif "token" in title_lower and "utility" in title_lower:
        return "تحديث جديد يخص فائدة التوكن واستخدامه."
    else:
        return None

# إرسال رسالة لتليجرام
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram Error: {e}")

# جلب الأخبار ومعالجتها
def fetch_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&public=true"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            send_to_telegram(f"❌ فشل جلب الأخبار: {response.status_code}")
            return
        news_items = response.json().get("results", [])
    except Exception as e:
        send_to_telegram("❌ خطأ في الاتصال بمصدر الأخبار.")
        return

    if not news_items:
        send_to_telegram("✅ تم الفحص: لا توجد أخبار حالياً.")
        return

    for item in news_items:
        title = item.get("title", "").strip()
        link = item.get("url", "").strip()
        rewritten = rewrite_human_friendly(title)

        if rewritten:
            message = f"{rewritten}\nالعنوان: {title or 'غير متوفر'}\n{link}"
        else:
            fallback_title = title if title else "لم يتم العثور على عنوان."
            message = f"عنوان مثير للاهتمام في سوق الكريبتو، التفاصيل في الخبر:\n{fallback_title}\n{link}"

        send_to_telegram(message)

# تشغيل البوت
if __name__ == "__main__":
    fetch_crypto_news()
