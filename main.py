import requests

# إعدادات البوت
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "af664841cdcd4c27a050b06660d1b2f0"

# فلترة الكلمات
TREND_KEYWORDS = ["pump", "hype", "trending", "viral", "explode", "surge", "moon"]
IMPORTANT_KEYWORDS = ["partnership", "launch", "update", "mainnet", "airdrop", "listing", "Binance", "Coinbase", "SEC"]

def send_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def translate_text(text):
    try:
        url = "https://libretranslate.de/translate"
        payload = {
            "q": text,
            "source": "en",
            "target": "ar",
            "format": "text"
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        return result["translatedText"]
    except Exception as e:
        return f"(ترجمة فشلت): {text}"

def classify_news(title):
    title_lower = title.lower()
    for word in TREND_KEYWORDS:
        if word in title_lower:
            return "خبر ترند"
    for word in IMPORTANT_KEYWORDS:
        if word in title_lower:
            return "خبر مهم"
    return None

def fetch_crypto():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&filter=hot"
    response = requests.get(url)
    data = response.json()

    if "results" in data and len(data["results"]) > 0:
        for post in data["results"]:
            title = post["title"]
            classification = classify_news(title)

            if classification:
                translated_title = translate_text(title)
                message = f"✅ {classification}:\n\n{translated_title}\n\nالمصدر: {post['url']}"
                send_message(message)
                break
        else:
            send_message("🔄 تم الفحص - فيه أخبار لكن ما فيها شي مهم أو ترند.")
    else:
        send_message("🔄 تم الفحص - ما فيه أخبار جديدة حالياً.")

# تشغيل البوت
send_message("✅ البوت اشتغل مع تصنيف الأخبار وإرسال تقارير كل 10 دقايق.")
fetch_crypto()
