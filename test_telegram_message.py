import requests

TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"

message = "هذه رسالة تجريبية من البوت. إذا وصلتك، فالبوت شغال تمام."

def send_test_message():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("[✓] تم إرسال الرسالة التجريبية بنجاح.")
    else:
        print(f"[!] فشل إرسال الرسالة، كود الاستجابة: {response.status_code}, الرد: {response.text}")

if __name__ == "__main__":
    send_test_message()
