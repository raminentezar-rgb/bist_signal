# notifier/telegram_bot.py
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# استفاده از لیست آیدی‌ها برای پشتیبانی از چند کانال/کاربر
CHAT_IDS = [cid.strip() for cid in os.getenv("TELEGRAM_CHAT_ID", "").split(",") if cid.strip()]

def send_telegram(message):
    for chat_id in CHAT_IDS:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode":"Markdown"})
        except Exception as e:
            print(f"Error sending to {chat_id}: {e}")

def send_chart(df, title="Chart"):
    plt.figure(figsize=(8,4))
    plt.plot(df)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("chart.png")
    plt.close()
    
    for chat_id in CHAT_IDS:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            with open("chart.png", "rb") as photo:
                requests.post(url, data={"chat_id": chat_id}, files={"photo": photo})
        except Exception as e:
            print(f"Error sending chart to {chat_id}: {e}")