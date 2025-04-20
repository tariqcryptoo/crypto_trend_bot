import requests

# بيانات البوت
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "9889e4a8021167e15bc0d74858809a6e0195fa2e"

# إعادة صياغة العنوان بلغة بشرية
def rewrite_human_friendly(title):
    title_lower = title.lower()

    if "airdrop" in title_lower:
        return "تم الإعلان عن Airdrop جديد، توزيع مجاني لعملة أو مشروع جديد في الكريبتو."
    elif "binance" in title_lower and "support" in title_lower:
        return "منصة Binance أعلنت دعم عملة جديدة، مما قد يؤثر على سعرها خلال الساعات القادمة."
    elif "launch" in title_lower or "released" in title_lower:
        return "إطلاق رسمي لمشروع أو منتج جديد في سوق الكريبتو، التفاصيل في الخبر."
    elif "whale" in title_lower and "sell" in title_lower:
        return "حوت كريبتو قام بعملية بيع كبيرة، قد تكون بسبب تراجع الأرباح أو توقع انخفاض."
    elif "hack" in title_lower or "exploit" in title_lower:
        return "تحذير: حصل اختراق أو ثغرة أمنية في أحد المشاريع، التفاصيل في الخبر."
    elif "partnership" in title_lower or "collaborat" in title_lower:
        return "فيه شراكة أو تعاون جديد بين شركات في عالم الكريبتو، مما قد يفتح فرص جديدة."
    elif "etf" in title_lower or "sec" in title_lower:
        return "تحديث يتعلق بصناديق ETF أو الجهات التنظيمية، ممكن يأثر على حركة السوق."
    elif "btc" in title_lower and "recovery" in title_lower:
        return "البيتكوين يشهد موجة تعافي في السعر، وسط تفاؤل حول السوق."
    elif "funding" in title_lower or "investment" in title_lower:
        return "استثمار جديد أو تمويل كبير تم الإعلان عنه في مشروع كريبتو."
    else:
        return "عنوان مثير للاهتمام في سوق الكريبتو، التفاصيل في الخبر."

# إرسال رسالة تيليجرام
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
        title = item.get("title", "")
        link = item.get("url", "")
        rewritten = rewrite_human_friendly(title)
        message = f"{rewritten}\n{link}"
        send_to_telegram(message)
        sent_anything = True

    if not sent_anything:
        send_to_telegram("✅ تم الفحص: لا يوجد أخبار حالياً تنطبق عليها الشروط.")

# تشغيل البوت
if __name__ == "__main__":
    fetch_crypto_news()
