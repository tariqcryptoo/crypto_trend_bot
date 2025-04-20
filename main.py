import requests

# بيانات الاتصال
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "9889e4a8021167e15bc0d74858809a6e0195fa2e"

# دالة إعادة الصياغة البشرية للخبر
def rewrite_human_friendly(title):
    title_lower = title.lower()

    if "airdrop" in title_lower:
        return f"تم الإعلان عن توزيع مجاني (Airdrop) لمشروع أو عملة. التفاصيل: {title}"
    elif "binance" in title_lower and "support" in title_lower:
        return f"منصة Binance أعلنت عن دعم رسمي لعملة جديدة. عنوان الخبر: {title}"
    elif "launch" in title_lower:
        return f"إطلاق جديد في السوق، مشروع أو منتج تم الإعلان عنه. التفاصيل: {title}"
    elif "partnership" in title_lower or "collaborat" in title_lower:
        return f"فيه شراكة جديدة بين جهات في سوق الكريبتو. العنوان: {title}"
    elif "hashrate" in title_lower or "mining" in title_lower:
        return f"تطور جديد في التعدين أو في معدل hashrate. نص الخبر: {title}"
    elif "etf" in title_lower or "sec" in title_lower:
        return f"خبر يخص صناديق ETF أو الجهات التنظيمية مثل SEC. مكتوب: {title}"
    elif "hack" in title_lower or "exploit" in title_lower:
        return f"تحذير من اختراق أو استغلال أمني في مشروع كريبتو. العنوان: {title}"
    elif "investment" in title_lower or "funding" in title_lower:
        return f"استثمار أو جولة تمويل جديدة في أحد المشاريع. التفاصيل: {title}"
    else:
        return f"خبر جديد في عالم الكريبتو: {title}"

# إرسال الرسائل إلى تيليجرام
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram error: {e}")

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
        send_to_telegram(f"❌ خطأ في الاتصال بمصدر الأخبار.")
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
        send_to_telegram("✅ تم الفحص: لا يوجد خبر حالياً ينطبق عليه الشروط.")

# تشغيل البوت
if __name__ == "__main__":
    fetch_crypto_news()
