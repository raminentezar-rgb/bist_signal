# main_auto.py

import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import pandas as pd
import matplotlib.pyplot as plt

from scanner.market_scanner import scan_market
from notifier.telegram_bot import send_telegram, send_chart
from strategies.trading import evaluate_signal

# ---------------- Main Function ----------------
def main():
    signals = scan_market()
    filtered_signals = []
    all_equity = []

    for signal in signals:
        symbol = signal['symbol']
        df = signal['df']
        df_bist = signal['df_bist']

        # ---------- فیلترهای Ultra-Professional ----------
        result = evaluate_signal(df, df_bist, require_breakout=False, require_vol_spike=False)

        if not result:
            continue

        # ذخیره برای جدول و نمودار جمعی
        filtered_signals.append({
            "symbol": symbol,
            "entry": result["entry"],
            "stop": result["stop"],
            "target": result["target"],
            "rs": round(result["rs"], 2),
            "winrate": round(result["winrate"], 2)
        })
        all_equity.append(result["equity"])


    # ---------- ارسال سیگنال‌ها به تلگرام ----------
    for s in filtered_signals:
        message = f"""
*BIST Ultra Swing Signal* 🚀

*Symbol:* {s['symbol']}
*Entry:* {s['entry']:.2f}
*Stop Loss:* {s['stop']:.2f}
*Target:* {s['target']:.2f}
*RS:* {s['rs']:.2f}
*WinRate:* {s['winrate']}%
"""
        send_telegram(message)

    # ---------- رسم Equity Curve جمعی ----------
    if all_equity:
        combined_equity = pd.concat(all_equity, axis=1).fillna(1).prod(axis=1)
        plt.figure(figsize=(10,5))
        plt.plot(combined_equity, label='Combined Equity Curve')
        plt.legend()
        plt.grid()
        plt.title('Combined Equity Curve - All Signals')
        plt.xlabel('Date')
        plt.ylabel('Equity')
        plt.tight_layout()
        plt.savefig('combined_equity.png')
        plt.close()
        send_chart(pd.DataFrame(combined_equity, columns=['Equity']), 'Combined_Equity')

    # ---------- جمع‌بندی روزانه ----------
    total_signals = len(filtered_signals)
    total_profit = sum((s['target']/s['entry']-1)*100 for s in filtered_signals)
    send_telegram(f"*Daily Ultra BIST Report* 📊\nTotal Signals: {total_signals}\nPotential Profit: {total_profit:.2f}%")

if __name__ == "__main__":
    main()