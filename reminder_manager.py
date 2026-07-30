import os
import json
from datetime import datetime
from config import REMINDERS_FILE

def load_reminders() -> list:
    if os.path.exists(REMINDERS_FILE):
        try:
            with open(REMINDERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Hatırlatıcılar yüklenirken hata: {e}")
            return []
    return []

def save_reminders(data: list):
    os.makedirs(os.path.dirname(REMINDERS_FILE), exist_ok=True)
    try:
        with open(REMINDERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Hatırlatıcılar kaydedilirken hata: {e}")

def add_reminder(time_str: str, text: str):
    reminders = load_reminders()
    new_reminder = {
        "time": time_str,
        "text": text,
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    }
    reminders.append(new_reminder)
    save_reminders(reminders)
    return True

def check_reminders_worker():
   
    pass
