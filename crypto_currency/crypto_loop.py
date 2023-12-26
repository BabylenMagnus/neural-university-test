import psycopg2
import requests

import schedule
import time
import threading
import os


conn = psycopg2.connect(
    dbname="postgres",
    user="user",
    password="secret",
    host="0.0.0.0",
    port=5432
)

cur = conn.cursor()
API_KEY = os.environ['']

cur.execute(
    "INSERT INTO database_cryptocurrencyprices (cryptocurrency_name, price) VALUES (%s, %s)",
    ("BTC", 41676.49)
)


def insert_crypto_price():
    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey={API_KEY}'
    r = requests.get(url).json()
    price = r["Realtime Currency Exchange Rate"]['5. Exchange Rate']

    cur.execute(
        "INSERT INTO database_cryptocurrencyprices (cryptocurrency_name, price) VALUES (%s, %s)",
        ("BTC", price)
    )

    conn.commit()


insert_crypto_price()


def run_continuously():
    schedule.every().hour.at(":00").do(insert_crypto_price)

    while True:
        schedule.run_pending()
        time.sleep(1)


schedule_thread = threading.Thread(target=run_continuously)
schedule_thread.start()
