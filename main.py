import requests
from deep_translator import GoogleTranslator

# إعداداتك
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "YOUR_CRYPTOPANIC_API_KEY"

# ترجمة ذكية
def translate_text(text):
    try:
        translated = GoogleTranslator(source='auto', target='ar').translate(text)
        # نحافظ على المصطلحات المهمة بدون ترجمتها
        keywords = ["Bitcoin", "Ethereum", "Binance", "Solana", "Airdrop", "NFT", "Arbitrum"]
        for word in keywords:
            translated = translated.replace(word.lower(), word).replace(word.upper(), word)
        return translated
    except:
        return text

# توليد ملخص إنساني بناءً على نوع الخبر
def generate_summary(tag):
    if tag == "🔵 Airdrop":
        return "خبر عن توزيع مجاني (Airdrop)، تابع التفاصيل إذا كنت من المستخدمين المؤهلين."
    elif tag == "⚒️ تعدين":
        return "تحديث يتعلق بالتعدين، قد يؤثر على شبكة العملة أو صعوبتها."
    elif tag == "🔥 ترند":
        return "الخبر عليه تفاعل كبير، وقد يكون مؤشر لتحرك السوق."
    elif tag == "📌 خبر مهم":
        return "خبر مهم في السوق، يستحق المتابعة لأنه متعلق بمؤسسات أو تغييرات كبيرة."
    else:
        return "تفاصيل خبر جديد في سوق الكريبتو."

# دوال التصنيف
def is_trending(news_item):
    return news_item.get("votes", {}).get("positive", 0) >= 20

def is_mining_related(text):
    keywords = ["mining", "hashrate", "asic", "antminer", "whatsminer"]
    return any(word in text.lower() for word in keywords)

def is_airdrop_related(text):
    keywords = ["airdrop", "claim", "snapshot", "retroactive", "free token"]
    return any(word in text.lower() for word in keywords)

def is_important(text):
    keywords = ["bitcoin", "ethereum", "binance", "sec", "etf", "coinbase", "blackrock"]
    return any(word in text.lower() for word in keywords)

# إرسال تيليجرام
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except:
        pass

# جلب الأخبار وتصنيفها
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

        if is_airdrop_related(title):
            tag = "🔵 Airdrop"
        elif is_mining_related(title):
            tag = "⚒️ تعدين"
        elif is_trending(item):
            tag = "🔥 ترند"
        elif is_important(title):
            tag = "📌 خبر مهم"
        else:
            continue

        translated_title = translate_text(title)
        summary = generate_summary(tag)

        msg = f"{tag}:\n{translated_title}\n{link}\n\n**تحليل:** {summary}"
        send_to_telegram(msg)
        sent_anything = True

    if not sent_anything:
        send_to_telegram("✅ تم الفحص: لا يوجد خبر ينطبق عليه الفلاتر حالياً.")

# تشغيل البوت
if __name__ == "__main__":
    fetch_crypto_news()
