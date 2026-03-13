# notifier/telegram_bot.py
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode":"Markdown"})

def send_chart(df, title="Chart"):
    plt.figure(figsize=(8,4))
    plt.plot(df)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("chart.png")
    plt.close()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open("chart.png", "rb") as photo:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": photo})