import requests
from typing import Any

from config import NEWS_API, COMPANY_NAME, NEWS_ENDPOINT


def fetch_news() -> list[dict[str, Any]]:
    params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API,
    }
    response = requests.get(NEWS_ENDPOINT, params=params, timeout=10)
    response.raise_for_status()
    return response.json()["articles"][:3]
