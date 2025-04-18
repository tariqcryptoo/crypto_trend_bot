import requests

# إعدادات البوت
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "af664841cdcd4c27a050b06660d1b2f0"

# الكلمات المفتاحية للتصنيف
TREND_KEYWORDS = ["pump", "hype", "trending", "viral", "explode", "surge", "moon"]
IMPORTANT_KEYWORDS = ["partnership", "launch", "update", "mainnet", "listing", "Binance", "Coinbase", "SEC"]
AIRDROP_MAIN = ["airdrop"]
AIRDROP_SUPPORT = ["eligible", "snapshot", "distribution", "claim", "confirmed", "binance", "launch", "token"]

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
    except Exception:
        return f"(ترجمة فشلت): {text}"

def classify_news(title):
    title_lower = title.lower()

    if any(main in title_lower for main in AIRDROP_MAIN) and any(support in title_lower for support in AIRDROP_SUPPORT):
        return "🎁 فرصة Airdrop"

    for word in TREND_KEYWORDS:
        if word in title_lower:
            return "✅ خبر ترند"

    for word in IMPORTANT_KEYWORDS:
        if word in title_lower:
            return "✅ خبر مهم"

    return None

def fetch_crypto():
    seen_links = []

    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&filter=hot"
    response = requests.get(url)
    data = response.json()

    if "results" in data and len(data["results"]) > 0:
        for post in data["results"]:
            title = post["title"]
            link = post["url"]

            if link in seen_links:
                continue

            classification = classify_news(title)
            if classification:
                translated_title = translate_text(title)
                message = f"{classification}:\n\n{translated_title}\n\nالمصدر: {link}"
                send_message(message)
                seen_links.append(link)
                break
        else:
            send_message("🔄 تم الفحص - فيه أخبار لكن كلها مكررة أو غير مهمة.")
    else:
        send_message("🔄 تم الفحص - ما فيه أخبار جديدة حالياً.")

# تشغيل البوت
send_message("✅ البوت اشتغل مع تصنيف Airdrop (المهم فقط) + ترند + مهم.")
fetch_crypto()
