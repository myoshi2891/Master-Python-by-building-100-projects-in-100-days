# 改善ポイント

1. **型ヒントを追加**
   `dict[str, Any]`, `list[dict[str, Any]]` などで明示。
2. **責務ごとに関数化**

   * `stock_service.py` … 株価取得
   * `news_service.py` … ニュース取得
   * `notifier.py` … Twilio通知
   * `main.py` … メインロジック
3. **環境変数の必須チェック**
   `os.getenv` の戻り値が `None` になる可能性を考慮。
4. **不要コメント削除**、エラーハンドリングを追加。

---

## リファクタリング後コード例

### `config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

STOCK_API: str = os.getenv("STOCK_API", "")
NEWS_API: str = os.getenv("NEWS_API", "")
TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
FROM_TWILIO: str = os.getenv("FROM_TWILIO", "")
TO_PHONE: str = os.getenv("TO_PHONE", "")

STOCK_NAME: str = "TSLA"
COMPANY_NAME: str = "Tesla Inc"
STOCK_ENDPOINT: str = "https://www.alphavantage.co/query"
NEWS_ENDPOINT: str = "https://newsapi.org/v2/everything"
```

---

### `stock_service.py`

```python
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
```

---

### `news_service.py`

```python
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
```

---

### `notifier.py`

```python
from typing import Sequence
from twilio.rest import Client

from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_TWILIO, TO_PHONE


def send_sms(messages: Sequence[str]) -> None:
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and FROM_TWILIO and TO_PHONE):
        raise ValueError("Twilio configuration is missing in environment variables.")

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for msg in messages:
        message = client.messages.create(
            body=msg,
            from_=FROM_TWILIO,
            to=TO_PHONE,
        )
        print(f"SMS sent to {message.to}: {message.body}")
```

---

### `main.py`

```python
from stock_service import fetch_stock_data
from news_service import fetch_news
# from notifier import send_sms  # Twilioを使う場合

from config import STOCK_NAME


def calculate_percentage_difference(stock_data: dict[str, dict[str, str]]) -> tuple[str, int]:
    data_list = list(stock_data.values())
    yesterday_close = float(data_list[0]["4. close"])
    day_before_close = float(data_list[1]["4. close"])
    difference = yesterday_close - day_before_close
    up_down = "🔺" if difference > 0 else "🔻"
    percentage_diff = round((difference / yesterday_close) * 100)
    return up_down, percentage_diff


def main() -> None:
    stock_data = fetch_stock_data()
    up_down, percentage_diff = calculate_percentage_difference(stock_data)

    if abs(percentage_diff) >= 5:
        articles = fetch_news()
        formatted_messages = [
            f"{STOCK_NAME}: {up_down}{percentage_diff}%\nHeadline: {article['title']}\nBrief: {article['description']}"
            for article in articles
        ]
        for msg in formatted_messages:
            print(msg)

        # Twilioで送信する場合
        # send_sms(formatted_messages)


if __name__ == "__main__":
    main()
```

---

## メリット

* **型安全**：Pylanceの警告が出ない。
* **責務分離**：ファイルごとに役割が明確。
* **保守性**：API変更や通知方法の変更に強い。
* **テスト容易性**：`stock_service`, `news_service` を単体でテスト可能。

---
