import requests

# بيانات الاتصال
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "9889e4a8021167e15bc0d74858809a6e0195fa2e"

# إعادة صياغة أي عنوان بشكل بشري مفهوم
def rewrite_human_friendly(title):
    title_lower = title.lower()

    if "airdrop" in title_lower:
        return f"فيه Airdrop جديد أعلنوا عنه لمشروع أو عملة. محتوى الخبر: {title}"
    elif "binance" in title_lower:
        return f"منصة Binance نشرت تحديث أو إعلان جديد. نص الخبر: {title}"
    elif "launch" in title_lower or "released" in title_lower:
        return f"فيه إطلاق أو منتج جديد في عالم الكريبتو. التفاصيل: {title}"
    elif "partner" in title_lower or "collaborat" in title_lower:
        return f"فيه تعاون أو شراكة بين شركات كريبتو. التفاصيل: {title}"
    elif "mining" in title_lower or "hashrate" in title_lower:
        return f"تحديث جديد في عالم التعدين أو معدل hashrate. نص العنوان: {title}"
    elif "etf" in title_lower or "sec" in title_lower:
        return f"الخبر يخص صناديق ETF أو التنظيمات مثل SEC. محتوى الخبر: {title}"
    elif "hack" in title_lower or "exploit" in title_lower:
        return f"تحذير! فيه اختراق أو استغلال أمني في مشروع كريبتو. العنوان: {title}"
    elif "funding" in title_lower or "investment" in title_lower:
        return f"فيه استثمار أو جولة تمويل جديدة في أحد المشاريع. نص الخبر: {title}"
    else:
        return f"عنوان جديد في الكريبتو تم تداوله اليوم. ممكن يحمل فرصة أو تحذير: {title}"

# إرسال تيليجرام
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except:
        pass

# جلب وتحليل الأخبار من CryptoPanic
def fetch_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&public=true"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            send_to_telegram(f"❌ فشل جلب الأخبار: {response.status_code}")
            return
        news_items = response.json().get("results", [])
    except:
        send_to_telegram("❌ خطأ في الاتصال بمصدر الأخبار.")
        return

    sent_anything = False

    for item in news_items:
        title = item.get("title", "")
        link = item.get("url", "")
        rewritten = rewrite_human_friendly(title)
        message = f"{rewritten}\n{link}"
        send_to_telegram(message)
        sent_anything = True

    if not sent_anything:
        send_to_telegram("✅ تم الفحص: لا يوجد خبر جديد حالياً.")

# تشغيل البوت
if __name__ == "__main__":
    fetch_crypto_news()p
