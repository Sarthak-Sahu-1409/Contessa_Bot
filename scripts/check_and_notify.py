import os
import requests
import datetime
from datetime import timezone

# Fetch secrets from environment variables
USER = os.environ['CLIST_USER']
KEY  = os.environ['CLIST_KEY']
TG_TOKEN = os.environ['TELEGRAM_TOKEN']
TG_CHAT  = os.environ['TELEGRAM_CHAT_ID']

# Platforms to track 
PLATFORMS = ["codeforces.com", "codechef.com", "leetcode.com", "atcoder.jp"]

def fetch_upcoming():
    """Fetches upcoming contests from the clist.by API."""
    url = "https://clist.by/api/v2/contest/"
    params = {
        "username": USER,
        "api_key": KEY,
        "limit": 5,
        "start__gte": datetime.datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "order_by": "start"
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json().get("objects", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching contests: {e}")
        return []

def send_telegram(text):
    """Sends a message to the specified Telegram chat."""
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT,
        "text": text,
        "parse_mode": "HTML" 
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Successfully sent notification for a contest.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")

if __name__ == '__main__':
    now_utc = datetime.datetime.now(timezone.utc)
    contests = fetch_upcoming()
    
    print(f"Found {len(contests)} upcoming contests. Checking for notifications...")

    for c in contests:
        # Parse the contest start time from the API response
        start_utc = datetime.datetime.fromisoformat(c['start']).replace(tzinfo=timezone.utc)
        delta = (start_utc - now_utc).total_seconds()
        
        # --- LOGIC CHANGE HERE ---
        # Check if the contest starts within the next 2 hours (7200 seconds)
        if 0 <= delta <= 22 * 60 * 60:
            resource = c['resource'].strip().lower()
            if resource in PLATFORMS:
                
                # --- PERSONALIZED MESSAGE ---
                
                # Convert UTC time to IST (UTC+5:30)
                ist_timezone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
                start_ist = start_utc.astimezone(ist_timezone)

                # Format times for readability
                time_utc_str = start_utc.strftime('%I:%M %p %Z')
                time_ist_str = start_ist.strftime('%I:%M %p IST')
                
                # Calculate remaining time
                hours, remainder = divmod(delta, 3600)
                minutes, _ = divmod(remainder, 60)
                
                msg = (
                    f"<b>🚀 Sarthak, Contest Alert! 🚀</b>\n\n"
                    f"<b>Contest:</b> {c['event']}\n"
                    f"<b>Platform:</b> {c['resource']}\n\n"
                    f"⏰ <b>Starts In:</b> {int(hours)} hrs {int(minutes)} mins\n"
                    f"🗓️ <b>Time:</b> {time_ist_str} ({time_utc_str})\n\n"
                    f"<a href='{c['href']}'>Go to Contest</a>"
                )
                
                send_telegram(msg)
    
    print("Check complete.")
