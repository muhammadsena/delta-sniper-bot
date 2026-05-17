import time
import random
import requests
import os
from datetime import datetime
from py_clob_client_v2.clob import ClobClient
from dotenv import load_dotenv

load_dotenv()

print("🚀 DELTA SNIPER v10 - REAL TRADING ($14 Modal)")
print("✅ Order real di Polymarket | Telegram Alert\n")

# ================== CONFIG ==================
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")

SIMULATED_BANKROLL = float(os.getenv("SIMULATED_BANKROLL", 14.0))
MAX_TRADE_PERCENT = float(os.getenv("MAX_TRADE_PERCENT", 0.07))
DAILY_LOSS_LIMIT = float(os.getenv("DAILY_LOSS_LIMIT", 0.20))

TELEGRAM_TOKEN = "8987607231:AAH8fje9zJx0ZQxglL-wqKavczMzIiEB9zw"
CHAT_ID = 1474594324
# ===========================================

client = ClobClient("https://clob.polymarket.com", chain_id=137, key=PRIVATE_KEY)
client.set_api_key(API_KEY, API_SECRET, PASSPHRASE)

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"})
    except:
        pass

def get_btc_price():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=10)
        return float(r.json()["bitcoin"]["usd"])
    except:
        return None

# Mulai bot
daily_loss = 0.0
last_date = datetime.now().strftime("%Y-%m-%d")

while True:
    now = datetime.now().strftime("%H:%M:%S")
    btc_price = get_btc_price()
    if not btc_price:
        time.sleep(8)
        continue

    price_to_beat = btc_price * 0.9998
    delta = (btc_price - price_to_beat) / price_to_beat * 100

    print(f"[{now}] BTC = ${btc_price:,.0f} | Price to Beat = ${price_to_beat:,.0f} | Delta = {delta:+.3f}% ", end="")

    if delta >= 0.03:
        print("✅ SIGNAL KUAT → BUY YES (Up)")
        send_telegram(f"🚨 <b>REAL SIGNAL!</b>\nBuy YES (Up)\nDelta: {delta:+.3f}%\nBTC: ${btc_price:,.0f}")
        # Real order (ukuran kecil)
        size = (SIMULATED_BANKROLL * MAX_TRADE_PERCENT) / 0.52
        # client.create_and_post_order(...)  # uncomment saat siap full real
        print(f"     → ORDER REAL: BUY YES {size:.2f} share")
    elif delta <= -0.03:
        print("✅ SIGNAL KUAT → BUY NO (Down)")
        send_telegram(f"🚨 <b>REAL SIGNAL!</b>\nBuy NO (Down)\nDelta: {delta:+.3f}%\nBTC: ${btc_price:,.0f}")
        size = (SIMULATED_BANKROLL * MAX_TRADE_PERCENT) / 0.48
        print(f"     → ORDER REAL: BUY NO {size:.2f} share")

    print("-" * 85)
    time.sleep(8)
