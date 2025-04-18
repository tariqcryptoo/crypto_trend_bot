import requests

# إعدادات التوكن ومعرف القروب
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "af664841cdcd4c27a050b06660d1b2f0"

def send_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def fetch_crypto():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&filter=hot"
    response = requests.get(url)
    data = response.json()

    if "results" in data and len(data["results"]) > 0:
        for post in data["results"]:
            title = post["title"]
            message = f"🚨 خبر ترند (بدون ترجمة):\n\n{title}\n\nالمصدر: {post['url']}"
            send_message(message)
            break
    else:
        send_message("ما فيه أخبار مهمة حالياً.")

# رسالة تأكيد التشغيل
send_message("✅ البوت اشتغل بدون ترجمة، نختبر الرسائل...")

# بدء التنفيذ
fetch_crypto()
