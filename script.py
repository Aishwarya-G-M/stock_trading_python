import requests
import os
from dotenv import load_dotenv
import time

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


