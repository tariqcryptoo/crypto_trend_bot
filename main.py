import requests

BOT_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = -4734806120

def send_test_message():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "✅ اختبار الاتصال بالتليجرام ناجح!"
    }
    response = requests.post(url, data=payload)
    print("Status:", response.status_code)
    print("Response:", response.text)

send_test_message()
