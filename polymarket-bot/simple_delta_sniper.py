import time
import random
import requests
import winsound
import os
from datetime import datetime

print("🚀 DELTA SNIPER DEMO MODE - THRESHOLD 0.015% (SUPER AGRESIF)")
print("✅ Sinyal akan muncul jauh lebih sering untuk testing\n")

# ================== TELEGRAM ==================
TELEGRAM_TOKEN = "8987607231:AAH8fje9zJx0ZQxglL-wqKavczMzIiEB9zw"
CHAT_ID = 1474594324
# =============================================

SIMULATED_BANKROLL = 14.0
ACTIVE_TRADE = None

os.makedirs("logs", exist_ok=True)

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"})
    except:
        pass

def play_alert_sound(is_buy=True):
    if is_buy:
        winsound.Beep(1200, 400)
        time.sleep(0.1)
        winsound.Beep(1400, 600)
    else:
        winsound.Beep(800, 400)
        time.sleep(0.1)
        winsound.Beep(600, 600)
    winsound.Beep(1000, 300)

def save_to_log(trade_data):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(f"logs/trade_{today}.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {trade_data}\n")

def get_btc_price():
    urls = [
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
        "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    ]
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                if "coingecko" in url:
                    return float(r.json()["bitcoin"]["usd"])
                else:
                    return float(r.json()["price"])
        except:
            continue
    return None

while True:
    now = datetime.now().strftime("%H:%M:%S")
    btc_price = get_btc_price()
    
    if not btc_price:
        print(f"[{now}] ⚠️ Gagal ambil harga BTC...")
        time.sleep(8)
        continue

    price_to_beat = btc_price * 0.9998
    delta = (btc_price - price_to_beat) / price_to_beat * 100

    print(f"[{now}] BTC = ${btc_price:,.0f} | P2B = ${price_to_beat:,.0f} | Delta = {delta:+.3f}% ", end="")

    if ACTIVE_TRADE is None:
        if delta >= 0.015:   # Threshold agresif untuk demo
            print("✅ SIGNAL → BUY YES (DEMO)")
            play_alert_sound(True)
            send_telegram(f"🚨 <b>DEMO SIGNAL!</b>\nBuy YES\nDelta: {delta:+.3f}%\nBTC: ${btc_price:,.0f}")
            entry_price = 0.52
            shares = SIMULATED_BANKROLL / entry_price
            ACTIVE_TRADE = {"side": "YES", "entry_price": entry_price, "shares": shares, "entry_time": time.time()}
            print(f"     → SIMULASI BELI {shares:.2f} share YES")
            save_to_log(f"BUY YES | Delta {delta:+.3f}%")
        elif delta <= -0.015:
            print("✅ SIGNAL → BUY NO (DEMO)")
            play_alert_sound(False)
            send_telegram(f"🚨 <b>DEMO SIGNAL!</b>\nBuy NO\nDelta: {delta:+.3f}%\nBTC: ${btc_price:,.0f}")
            entry_price = 0.48
            shares = SIMULATED_BANKROLL / entry_price
            ACTIVE_TRADE = {"side": "NO", "entry_price": entry_price, "shares": shares, "entry_time": time.time()}
            print(f"     → SIMULASI BELI {shares:.2f} share NO")
            save_to_log(f"BUY NO | Delta {delta:+.3f}%")
        else:
            print("⏳ Menunggu delta ≥ 0.015%...")
    else:
        hold_time = time.time() - ACTIVE_TRADE["entry_time"]
        if hold_time >= random.randint(60, 120):
            profit_per_share = random.uniform(0.08, 0.15)
            exit_price = ACTIVE_TRADE["entry_price"] + profit_per_share
            profit = ACTIVE_TRADE["shares"] * profit_per_share
            print(f"     → JUAL {ACTIVE_TRADE['side']} @ {exit_price:.2f}¢ → Profit +${profit:.2f}")
            SIMULATED_BANKROLL += profit
            print(f"     💰 Modal sekarang: ${SIMULATED_BANKROLL:.2f}\n")
            send_telegram(f"✅ Demo Trade Selesai!\nJual {ACTIVE_TRADE['side']} → Profit +${profit:.2f}\nModal: ${SIMULATED_BANKROLL:.2f}")
            save_to_log(f"JUAL {ACTIVE_TRADE['side']} → Profit +${profit:.2f}")
            ACTIVE_TRADE = None
        else:
            print(f"     ⏳ Sedang hold {ACTIVE_TRADE['side']} ({hold_time:.0f}s)")

    print("-" * 85)
    time.sleep(8)
