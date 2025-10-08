import os
import requests

# Load secrets from environment
TG_TOKEN = os.environ['TELEGRAM_TOKEN']
TG_CHATS = os.environ['TELEGRAM_CHAT_IDS'].split(",")

def send_debug_message():
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    text = "👋 Hi! I am the bot made by Sarthak Sahu. I will notify you about upcoming contests!"
    
    for chat_id in TG_CHATS:
        payload = {
            "chat_id": chat_id.strip(),
            "text": text,
            "parse_mode": "HTML"
        }
        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            print(f"✅ Message sent to chat ID {chat_id}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending to {chat_id}: {e}")

if __name__ == "__main__":
    send_debug_message()
