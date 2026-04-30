import requests
import os
from dotenv import load_dotenv
import time
import csv

load_dotenv()  # Load environment variables from .env file

MASSIVE_API_KEY = os.getenv("MASSIVE_API_KEY")

# print(" remove the api key from here!!!!")

# print("API key loaded from .env file:", MASSIVE_API_KEY)
LIMIT = 1000

url = f"https://api.massive.com/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={MASSIVE_API_KEY}"

#url = f"https://api.massive.com/v3/reference/tickers?market=stocks&active=true&order=asc&limit=1000000&sort=ticker&apiKey={MASSIVE_API_KEY}" 
# paginated api hence exceeding limit value will cause error.

response = requests.get(url)
data = response.json()
tickers = []

for ticker in data['results']:
    tickers.append(ticker)


while 'next_url' in data:
    time.sleep(12)
    print('requesting next page of data...')
    response = requests.get(data['next_url'] + f'&apiKey={MASSIVE_API_KEY}')
    data = response.json()
    print(data)
    if 'results' not in data:
        print("Unexpected response:", data)
        break
    tickers.extend(data["results"])
    
print(len(tickers))

example_ticker = {
    "ticker": "ZYME",
    "name": "Zymeworks Inc.",
    "market": "stocks",
    "locale": "us",
    "primary_exchange": "XNAS",
    "type": "CS",
    "active": True,
    "currency_name": "usd",
    "cik": "0001937653",
    "composite_figi": "BBG019XSYC89",
    "share_class_figi": "BBG019XSYC98",
    "last_updated_utc": "2026-04-29T06:09:42.02927038Z",
}

fieldnames = example_ticker.keys()
output_file = "tickers.csv"

with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for ticker in tickers:
        row = {field: ticker.get(field, "") for field in fieldnames}
        writer.writerow(row)

print(f'Wrote {len(tickers)} rows to {output_file}')


