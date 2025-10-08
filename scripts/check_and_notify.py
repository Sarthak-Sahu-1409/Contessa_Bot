import os
import requests
import datetime

# Fetch secrets
USER = os.environ['CLIST_USER']
KEY  = os.environ['CLIST_KEY']
TG_TOKEN = os.environ['TELEGRAM_TOKEN']
TG_CHAT  = os.environ['TELEGRAM_CHAT_ID']

# Platforms to track (lowercase for safe comparison)
PLATFORMS = ["codeforces", "codechef", "leetcode", "atcoder"]

def fetch_upcoming():
    url = "https://clist.by/api/v2/contest/"
    params = {
        "username": USER,
        "api_key": KEY,
        "limit": 100,
        "start__gte": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
        "order_by": "start"
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json().get("objects", [])

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TG_CHAT, "text": text})

if __name__ == '__main__':
    now = datetime.datetime.utcnow()
    contests = fetch_upcoming()
    
    for c in contests:
        # Debug: see what 'resource' is
        print(c['resource'], c['event'], c['start'])
        
        start = datetime.datetime.fromisoformat(c['start'])
        delta = (start - now).total_seconds()
        
        if 0 <= delta <= 24*60*60:
            # Case-insensitive check
            if c['resource'].strip().lower() in PLATFORMS:
                msg = (
                    f"⏰ Upcoming Contest!\n\n"
                    f"{c['event']} on {c['resource']}\n"
                    f"Starts at {c['start']} UTC "
                    f"(in ~{int(delta//3600)} hrs {int((delta%3600)//60)} mins)"
                )
                send_telegram(msg)
