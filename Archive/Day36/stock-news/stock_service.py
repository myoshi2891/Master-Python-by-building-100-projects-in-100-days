import requests
from typing import Any

from config import STOCK_API, STOCK_NAME, STOCK_ENDPOINT


def fetch_stock_data() -> dict[str, Any]:
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK_NAME,
        "apikey": STOCK_API,
    }
    response = requests.get(STOCK_ENDPOINT, params=params, timeout=10)
    response.raise_for_status()
    return response.json()["Time Series (Daily)"]
