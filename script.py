import requests
import os
from dotenv import load_dotenv

load_dotenv()

print("hello world")
LIMIT = 100
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&offset=0&sort=ticker&apiKey={POLYGON_API_KEY}"

response = requests.get(url)
tickers = []

data = response.json()
for ticker in data["results"]:
    tickers.append(ticker)

while 'next_url' in data:
    print('requiring next page', data['next_url'])
    response = requests.get(data['next_url'] + f"&apiKey={POLYGON_API_KEY}")
    data = response.json()
    print(data)
    for ticker in data["results"]:
        tickers.append(ticker)

print(len(tickers))