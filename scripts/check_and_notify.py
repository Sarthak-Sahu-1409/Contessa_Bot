import os
import requests
import datetime

# Fetch secrets
USER = os.environ['CLIST_USER']
KEY  = os.environ['CLIST_KEY']
TG_TOKEN = os.environ['TELEGRAM_TOKEN']
TG_CHAT  = os.environ['TELEGRAM_CHAT_ID']

# Fetch upcoming contests from CLIST API
def fetch_upcoming():
    url = "https://clist.by/api/v2/contest/"
    params = {
        "username": USER,
        "api_key": KEY,
        "limit": 50,
        "start__gte": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
        "order_by": "start"
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json().get("objects", [])

# Send Telegram message
def send_telegram(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TG_CHAT, "text": text})

if __name__ == '__main__':
    now = datetime.datetime.utcnow()
    contests = fetch_upcoming()
    for c in contests:
        start = datetime.datetime.fromisoformat(c['start'])
        delta = (start - now).total_seconds()
        # Notify if contest starts in about 1 hour (±5 min)
        if 55*60 <= delta <= 65*60:
            msg = f"⏰ Reminder!\n\n{c['event']} on {c['resource']}\nStarts at {c['start']} UTC (≈1 hr)"
            send_telegram(msg)
