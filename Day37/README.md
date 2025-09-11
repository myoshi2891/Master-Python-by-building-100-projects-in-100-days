# 改善ポイント

1. **型付け**

   - `Optional[str]` を使って環境変数を安全に扱う
   - 関数の戻り値に `requests.Response` 型を付与

2. **関数分割**

   - Pixela ユーザー作成、グラフ作成、ピクセル作成・更新・削除を関数化

3. **ファイル分割提案**

   - `pixela_client.py`: Pixela API の関数群
   - `main.py`: 実行部分（ユーザー入力や実行フロー）

---

## リファクタリング後のコード（単一ファイル版）

```python
import os
from typing import Optional
from datetime import datetime

import requests
from requests import Response
from dotenv import load_dotenv

load_dotenv()

TOKEN: Optional[str] = os.getenv("TOKEN")
USERNAME: Optional[str] = os.getenv("USERNAME")
GRAPH_ID: str = "graph2"

PIXELA_URL = "https://pixe.la/v1/users"


def create_user(token: str, username: str) -> Response:
    user_params = {
        "token": token,
        "username": username,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    return requests.post(url=PIXELA_URL, json=user_params)


def create_graph(token: str, username: str, graph_id: str) -> Response:
    graph_endpoint = f"{PIXELA_URL}/{username}/graphs"
    graph_config = {
        "id": graph_id,
        "name": "Algorithm Graph",
        "unit": "hours",
        "type": "int",
        "color": "ajisai",
    }
    headers = {"X-USER-TOKEN": token}
    return requests.post(url=graph_endpoint, json=graph_config, headers=headers)


def create_pixel(token: str, username: str, graph_id: str, date: datetime, quantity: str) -> Response:
    pixel_endpoint = f"{PIXELA_URL}/{username}/graphs/{graph_id}"
    pixel_data = {
        "date": date.strftime("%Y%m%d"),
        "quantity": quantity,
    }
    headers = {"X-USER-TOKEN": token}
    return requests.post(url=pixel_endpoint, json=pixel_data, headers=headers)


def update_pixel(token: str, username: str, graph_id: str, date: datetime, quantity: str) -> Response:
    update_endpoint = f"{PIXELA_URL}/{username}/graphs/{graph_id}/{date.strftime('%Y%m%d')}"
    pixel_update_data = {"quantity": quantity}
    headers = {"X-USER-TOKEN": token}
    return requests.put(url=update_endpoint, json=pixel_update_data, headers=headers)


def delete_pixel(token: str, username: str, graph_id: str, date: datetime) -> Response:
    delete_endpoint = f"{PIXELA_URL}/{username}/graphs/{graph_id}/{date.strftime('%Y%m%d')}"
    headers = {"X-USER-TOKEN": token}
    return requests.delete(url=delete_endpoint, headers=headers)


def main() -> None:
    if TOKEN is None or USERNAME is None:
        raise ValueError("環境変数 TOKEN または USERNAME が設定されていません。")

    today = datetime(year=2025, month=5, day=6)

    # ピクセル作成
    hours = input("How many hours did you study today? ")
    response = create_pixel(TOKEN, USERNAME, GRAPH_ID, today, hours)
    print("Pixel Creation:", response.text)

    # ピクセル更新
    response = update_pixel(TOKEN, USERNAME, GRAPH_ID, today, "15")
    print("Pixel Update:", response.text)

    # ピクセル削除
    response = delete_pixel(TOKEN, USERNAME, GRAPH_ID, today)
    print("Pixel Delete:", response.text)


if __name__ == "__main__":
    main()
```

---

## ファイル分割する場合の提案

### `pixela_client.py`

Pixela API 操作をまとめる。

### `main.py`

ユーザー入力や処理の流れを記述。

---

👉 こうすることで、Pylance エラーは消え、関数ごとに役割が明確になります。

責務を分けて：

- **pixela_client.py** : Pixela API を叩く関数群（create, update, delete を含む）
- **main.py** : 実行部分。学習時間を入力して「追加・更新・削除」を選べる CLI

---

### `pixela_client.py`

```python
import requests
from requests import Response
from datetime import datetime

PIXELA_URL = "https://pixe.la/v1/users"


def create_pixel(token: str, username: str, graph_id: str, date: datetime, quantity: str) -> Response:
    """指定した日付に学習時間を記録する"""
    pixel_endpoint = f"{PIXELA_URL}/{username}/graphs/{graph_id}"
    pixel_data = {
        "date": date.strftime("%Y%m%d"),
        "quantity": quantity,
    }
    headers = {"X-USER-TOKEN": token}
    return requests.post(url=pixel_endpoint, json=pixel_data, headers=headers)


def update_pixel(token: str, username: str, graph_id: str, date: datetime, quantity: str) -> Response:
    """指定した日付の学習時間を更新する"""
    update_endpoint = f"{PIXELA_URL}/{username}/graphs/{graph_id}/{date.strftime('%Y%m%d')}"
    pixel_update_data = {"quantity": quantity}
    headers = {"X-USER-TOKEN": token}
    return requests.put(url=update_endpoint, json=pixel_update_data, headers=headers)


def delete_pixel(token: str, username: str, graph_id: str, date: datetime) -> Response:
    """指定した日付の学習時間を削除する"""
    delete_endpoint = f"{PIXELA_URL}/{username}/graphs/{graph_id}/{date.strftime('%Y%m%d')}"
    headers = {"X-USER-TOKEN": token}
    return requests.delete(url=delete_endpoint, headers=headers)
```

---

## `main.py`

```python
import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from pixela_client import create_pixel, update_pixel, delete_pixel

load_dotenv()

TOKEN: Optional[str] = os.getenv("TOKEN")
USERNAME: Optional[str] = os.getenv("USERNAME")
GRAPH_ID: str = "graph2"


def main() -> None:
    if TOKEN is None or USERNAME is None:
        raise ValueError("環境変数 TOKEN または USERNAME が設定されていません。")

    today = datetime.now()
    print("=== Pixela 学習時間管理 ===")
    print("1: 新規追加 (create)")
    print("2: 更新 (update)")
    print("3: 削除 (delete)")

    choice = input("操作を選んでください (1/2/3): ").strip()

    if choice == "1":
        hours = input("今日の学習時間を入力してください (h): ")
        response = create_pixel(TOKEN, USERNAME, GRAPH_ID, today, hours)
        print("Pixel Creation:", response.text)

    elif choice == "2":
        hours = input("修正後の学習時間を入力してください (h): ")
        response = update_pixel(TOKEN, USERNAME, GRAPH_ID, today, hours)
        print("Pixel Update:", response.text)

    elif choice == "3":
        confirm = input("本当に削除しますか？ (y/n): ").lower()
        if confirm == "y":
            response = delete_pixel(TOKEN, USERNAME, GRAPH_ID, today)
            print("Pixel Delete:", response.text)
        else:
            print("削除をキャンセルしました。")

    else:
        print("無効な選択です。終了します。")


if __name__ == "__main__":
    main()
```

---

## 実行イメージ

```bash
$ python main.py
=== Pixela 学習時間管理 ===
1: 新規追加 (create)
2: 更新 (update)
3: 削除 (delete)
操作を選んでください (1/2/3): 1
今日の学習時間を入力してください (h): 3
Pixel Creation: {"message":"Success","isSuccess":true}
```

---

これで「**日ごとに create しつつ、誤入力したら update、不要なら delete**」というフローを一つの CLI で回せます。
