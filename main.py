import requests

# بيانات البوت
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "9889e4a8021167e15bc0d74858809a6e0195fa2e"

# دالة إعادة الصياغة البشرية مع العنوان
def rewrite_human_friendly(title):
    title_lower = title.lower()

    if "airdrop" in title_lower:
        return "تم الإعلان عن Airdrop جديد لمشروع كريبتو، تابع التفاصيل."
    elif "binance" in title_lower and "support" in title_lower:
        return "منصة Binance أعلنت دعم لعملة أو مشروع جديد، مما قد يؤثر على سعره."
    elif "whale" in title_lower and "sell" in title_lower:
        return "حوت كريبتو باع كمية كبيرة من العملات، وقد يؤثر ذلك على السوق."
    elif "launch" in title_lower or "released" in title_lower:
        return "إطلاق رسمي لمنتج أو مشروع جديد في عالم الكريبتو."
    elif "testnet" in title_lower or "mainnet" in title_lower:
        return "تم إطلاق شبكة اختبارية أو رئيسية لمشروع جديد."
    elif "etf" in title_lower or "sec" in title_lower:
        return "الخبر يتعلق بصناديق ETF أو بتحديث تنظيمي من هيئة SEC."
    elif "partnership" in title_lower or "collaborat" in title_lower:
        return "فيه شراكة جديدة بين كيانات كريبتو، ممكن تفتح فرص كبيرة."
    elif "hack" in title_lower or "exploit" in title_lower:
        return "تحذير: حصل اختراق أو استغلال ثغرة أمنية."
    elif "btc" in title_lower and "recovery" in title_lower:
        return "البيتكوين يشهد موجة تعافي، مع تفاؤل بإمكانية تجاوز حاجز 100,000 دولار."
    elif "investment" in title_lower or "funding" in title_lower:
        return "تم الإعلان عن استثمار أو جولة تمويل كبيرة لمشروع جديد."
    elif "token" in title_lower and "utility" in title_lower:
        return "تحديث جديد يخص فائدة واستخدام التوكن في أحد المشاريع."
    else:
        return None  # غير مفهوم تمامًا

# إرسال رسالة إلى تيليجرام
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram Error: {e}")

# جلب وتحليل الأخبار
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

    sent_anything = False

    for item in news_items:
        title = item.get("title", "").strip()
        link = item.get("url", "").strip()

        rewritten = rewrite_human_friendly(title)

        if rewritten:
            message = f"{rewritten}\nالعنوان: {title}\n{link}"
        else:
            message = f"الخبر غير واضح تمامًا لكن عنوانه:\n{title}\n{link}"

        send_to_telegram(message)
        sent_anything = True

    if not sent_anything:
        send_to_telegram("✅ تم الفحص: لا يوجد أخبار حالياً تنطبق عليها الشروط.")

# تشغيل البوت
if __name__ == "__main__":
    fetch_crypto_news()
