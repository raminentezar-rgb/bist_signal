# run_scheduler.py

import schedule
import time
import pytz
from datetime import datetime
import subprocess

# Istanbul Zaman Dilimi
IST = pytz.timezone('Europe/Istanbul')

def job():
    print(f"\n[{datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')}] 🚀 BIST Botu otomatik olarak baslatiliyor...")
    try:
        # Ana bot dosyasini çalistir
        subprocess.run(["python", "main_auto.py"], check=True)
        print(f"[{datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')}] ✅ Piyasa taramasi tamamlandi.")
    except Exception as e:
        print(f"❌ Bot çalistirilirken hata olustu: {e}")

def schedule_by_ist_time():
    """
    Pazartesi'den Cuma'ya kadar saat 17:50'de (Istanbul saati) botu çalistirir.
    """
    schedule.every().monday.at("17:50").do(job)
    schedule.every().tuesday.at("17:50").do(job)
    schedule.every().wednesday.at("17:50").do(job)
    schedule.every().thursday.at("17:50").do(job)
    schedule.every().friday.at("17:50").do(job)

if __name__ == "__main__":
    schedule_by_ist_time()
    print("⏳ Otomatik bot baslatildi...")
    print("Botun zamaninda çalisabilmesi için bu pencerenin açik kalmasi gerekir.")
    print("Zamanlama: Pazartesi - Cuma, Saat 17:50 (Istanbul). Bekleniyor...\n")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

