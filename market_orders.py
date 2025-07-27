import os
import sys
import logging
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

print("KEY:", API_KEY)
print("SECRET:", API_SECRET)

# Setup client
client = Client(API_KEY, API_SECRET)
client.FUTURES_URL = "https://testnet.binancefuture.com"

# Logging
logging.basicConfig(filename="bot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Validate input
if len(sys.argv) != 4:
    print("Usage: python market_orders.py SYMBOL SIDE QUANTITY")
    sys.exit()

symbol = sys.argv[1].upper()
side = sys.argv[2].upper()
quantity = float(sys.argv[3])

try:
    # Debug: Check balance
    balance = client.futures_account_balance()
    usdt = next(item for item in balance if item["asset"] == "USDT")
    print(f"✅ Testnet Balance: {usdt['balance']} USDT")

    # Place market order
    order = client.futures_create_order(
        symbol=symbol,
        side=SIDE_BUY if side == "BUY" else SIDE_SELL,
        type=ORDER_TYPE_MARKET,
        quantity=quantity,
        recvWindow=60000
    )

    print("✅ Market Order Placed Successfully!")
    print(order)
    logging.info(f"Market Order: {order}")

except BinanceAPIException as e:
    print(f"❌ Binance API Error: {e.message}")
    logging.error(f"API ERROR: {e}")
except Exception as e:
    print(f"❌ General Error: {e}")
    logging.error(f"GENERAL ERROR: {e}")
