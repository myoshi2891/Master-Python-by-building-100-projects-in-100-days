# HTTP ヘッダーについて

## HTTP ヘッダーの全体的な目的

まず、これらのヘッダー全体に共通する目的は、**「Python スクリプトからのリクエストを、人間が操作する本物の Web ブラウザからのリクエストに見せかけること」**です。

Amazon のような大規模な Web サイトは、ボットやスクレイピングによる自動アクセスを検知し、ブロックしようとします。`requests`ライブラリがデフォルトで送信するリクエストは非常にシンプルで、いかにもプログラムからのアクセスだとバレてしまいます。そこで、これらのヘッダーを追加することで、サーバーを「騙し」、正常なコンテンツ（この場合は商品ページ）を取得しやすくします。

---

## 各ヘッダーの詳細解説

### 1. `User-Agent`

```text
"User-Agent": USER_AGENT,
```

- **意味**: リクエストを送信しているクライアント（ブラウザ、アプリ、スクリプトなど）の種類をサーバーに伝えるための識別情報です。`USER_AGENT`変数には、おそらく`"Mozilla/5.0 (Windows NT 10.0; Win64; x64) ..."`のような、Chrome や Safari などの一般的なブラウザを名乗る文字列が格納されています。
- **重要性**: **これは最も重要なヘッダーです。** `User-Agent`が設定されていない、または`python-requests`のようなデフォルト値のままだと、サーバーは即座に「これはボットだ」と判断し、アクセスを拒否（403 Forbidden エラー）したり、CAPTCHA（画像認証）ページを表示したりします。本物のブラウザの`User-Agent`を設定することで、この最初のブロックを回避できます。

### 2. `Accept-Language`

```text
"Accept-Language": "ja;q=0.2,en-US,en;q=0.9",
```

- **意味**: クライアントが理解できる言語とその優先順位をサーバーに伝えます。
  - `en-US` (アメリカ英語) と `en` (英語) を最も優先 (`q=0.9`) します。`q`は品質値（quality value）で、優先度を示します (0〜1)。
  - `ja` (日本語) も受け入れ可能ですが、優先度は低い (`q=0.2`) です。
- **重要性**: サーバーは、この情報に基づいて表示するページの言語を決定します。例えば、Amazon.com にアクセスした場合でも、このヘッダーに応じて英語のページを返すようになります。これにより、特定の言語設定を持つユーザーからのリクエストであるように見せかけることができます。

### 3. `Accept`

```text
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
```

- **意味**: クライアントが受信して処理できるコンテンツの種類（MIME タイプ）をサーバーに伝えます。
  - `text/html`, `application/xhtml+xml`: HTML ドキュメント。
  - `image/avif`, `image/webp`, `image/apng`: 最新の画像フォーマット。
  - `*/*;q=0.8`: 上記以外でも、あらゆる種類を 8 割方の優先度で受け入れる。
- **重要性**: 現代のブラウザは多様なコンテンツタイプを処理できるため、このように詳細な`Accept`ヘッダーを送ることで、リクエストが本物のブラウザから来たものであると見せかける信憑性が高まります。

### 4. `Cache-Control`

```text
"Cache-Control": "max-age=0",
```

- **意味**: キャッシュの挙動を制御します。`max-age=0`は、「キャッシュされたコンテンツは使わず、必ずサーバーから最新のコンテンツを取得してほしい」という要求です。ユーザーがブラウザでリロードボタン（Ctrl+R や Cmd+R）を押したときと同様の挙動です。
- **重要性**: スクレイピングでは、常に最新の価格や在庫情報を取得したいため、キャッシュではなく最新の情報を要求することが理にかなっています。

### 5. `Upgrade-Insecure-Requests`

```text
"Upgrade-Insecure-Requests": "1",
```

- **意味**: クライアントが、暗号化されていない HTTP リクエストを、暗号化された HTTPS リクエストにアップグレードする意向があることをサーバーに伝えます。
- **重要性**: 最近のブラウザは標準でこのヘッダーを送信します。これを含めることで、セキュリティを意識した現代的なブラウザからのリクエストであることをアピールできます。

### 6. `Sec-Fetch-Site`

```text
"Sec-Fetch-Site": "none",
```

- **意味**: このリクエストがどのようにして発生したかを示します。`none`は、ユーザーがブラウザのアドレスバーに URL を直接入力した、またはブックマークから開いたなど、他のサイトからの遷移（リファラ）なしに開始されたリクエストであることを意味します。
- **重要性**: これは比較的新しいセキュリティ関連のヘッダー（Fetch Metadata Request Headers）の一つです。これを正しく設定することで、より巧妙にブラウザの挙動を模倣できます。

### 7. `Sec-Fetch-Mode`

```text
"Sec-Fetch-Mode": "navigate",
```

- **意味**: リクエストのモードを示します。`navigate`は、トップレベルの文書（HTML ページなど）を取得するためのナビゲーションリクエストであることを意味します。
- **重要性**: `Sec-Fetch-Site`と同様に、リクエストの意図をサーバーに伝え、通常のブラウジング操作の一部であるように見せかけるためのヘッダーです。

## まとめ

これらのヘッダーは、一つ一つが「私は普通のユーザーが使っているブラウザです」とサーバーに伝えるためのパズルのピースのようなものです。これらを組み合わせることで、スクレイピングがブロックされる可能性を大幅に減らし、目的のデータを安定して取得できるようになります。

### リファクタリングの方針

1. **型ヒントの追加**: すべての変数、関数の引数、戻り値に型ヒントを付け、コードの可読性と安全性を向上させます。
2. **関数の分割**: ロジックを「データ取得」「メール送信」「メイン処理」の 3 つの関数に分割し、責務を明確にします。
3. **エラーハンドリングの強化**:
    - Web サイトからのデータ取得失敗（ネットワークエラー、HTML 構造の変更など）を考慮します。
    - 価格やタイトルの要素が見つからない場合にプログラムがクラッシュしないようにします。
    - メール送信時のエラーを捕捉します。
4. **定数の整理**: URL や目標価格などを定数としてまとめ、管理しやすくします。
5. **メイン処理の明確化**: `if __name__ == "__main__":` を使用して、スクリプトとして実行されるエントリーポイントを定義します。

---

### リファクタリング後のコード

以下に、リファクタリングしたコードを提案します。

```python
import smtplib
import sys
from typing import Dict, Optional, Tuple

import requests
from bs4 import BeautifulSoup, Tag
from config import E_MAIL, E_MAIL2, PASSWORD, SMTP_ADDRESS, USER_AGENT

# ====================== Constants ===========================

PRODUCT_URL: str = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
BUY_PRICE: float = 100.0
REQUEST_HEADERS: Dict[str, str] = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",  # To get consistent price format ($)
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
}


def fetch_product_data(url: str, headers: Dict[str, str]) -> Optional[Tuple[float, str]]:
    """Fetches product price and title from the given URL."""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    price_element: Optional[Tag] = soup.find(class_="a-offscreen")
    title_element: Optional[Tag] = soup.find(id="productTitle")

    if not price_element or not title_element:
        print("Could not find price or title element. The page layout may have changed.")
        return None

    price_str: str = price_element.get_text()
    title: str = title_element.get_text().strip()

    try:
        # Remove currency symbols like '$' and convert to float
        price_without_currency = "".join(filter(lambda char: char.isdigit() or char == '.', price_str))
        price_as_float = float(price_without_currency)
        return price_as_float, title
    except (ValueError, IndexError) as e:
        print(f"Could not parse the price: {price_str}. Error: {e}")
        return None


def send_email_alert(product_title: str, current_price: float) -> None:
    """Sends an email alert if the price is below the target."""
    message = f"{product_title} is now only ${current_price}!\n\nCheck it out here:\n{PRODUCT_URL}"
    email_content = f"Subject:Amazon Price Alert!\n\n{message}".encode("utf-8")

    try:
        with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
            connection.starttls()
            connection.login(user=E_MAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=E_MAIL,
                to_addrs=E_MAIL2,
                msg=email_content,
            )
        print("Email alert sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")


def main() -> None:
    """Main function to check product price and send an alert."""
    if not all([E_MAIL, E_MAIL2, PASSWORD, SMTP_ADDRESS, USER_AGENT]):
        print("One or more environment variables are not set. Exiting.")
        sys.exit(1)

    product_data = fetch_product_data(PRODUCT_URL, REQUEST_HEADERS)

    if product_data is None:
        print("Failed to retrieve product data. Exiting.")
        sys.exit(1)

    price_as_float, title = product_data
    print(f"Retrieved product: {title}")
    print(f"Current price: ${price_as_float}")

    if price_as_float < BUY_PRICE:
        print(f"Price is below ${BUY_PRICE}. Sending an email alert...")
        send_email_alert(product_title=title, current_price=price_as_float)
    else:
        print(f"Price is not below the target of ${BUY_PRICE}.")


if __name__ == "__main__":
    main()
```

### 主な変更点の解説

1. **型ヒントの導入**:

    - `typing`モジュールから`Dict`, `Optional`, `Tuple`をインポートし、辞書や「None の可能性がある型」などを明示しました。
    - `fetch_product_data`の戻り値は `Optional[Tuple[float, str]]` となり、「価格(float)とタイトル(str)のタプル」または「失敗を示す`None`」を返すことが明確になりました。

2. **関数の分割**:

    - `fetch_product_data`: Web スクレイピングのロジックをカプセル化しました。成功すれば価格とタイトルを、失敗すれば`None`を返します。
    - `send_email_alert`: メール送信のロジックをまとめました。
    - `main`: 全体の処理の流れを制御します。

3. **エラーハンドリングの改善**:

`fetch_product_data`内で`requests`ライブラリを使用する際のエラーハンドリングを強化しました。

- **`requests.RequestException`の捕捉**:
  `requests.get()`を`try...except`ブロックで囲むことで、ネットワーク接続の問題（例: DNS 解決失敗、タイムアウト）や、サーバーからの不正なレスポンス（例: 4xx, 5xx エラー）など、HTTP リクエストに関するあらゆる例外を`requests.RequestException`として捕捉します。これにより、スクレイピングの最初のステップで失敗してもプログラムがクラッシュするのを防ぎます。

- **`response.raise_for_status()`の利用**:
  リクエストが成功しても、ステータスコードが`200 OK`でない場合があります（例: `404 Not Found`や`403 Forbidden`）。`response.raise_for_status()`は、ステータスコードが 400 番台または 500 番台の場合に`HTTPError`例外を発生させます。これを`try...except`ブロックで捕捉することで、リクエストが成功しなかったケースを確実に検知できます。

- **要素が見つからない場合の処理**:
  `soup.find()`は、指定された要素が見つからない場合に`None`を返します。`if not price_element or not title_element:`というチェックを入れることで、Amazon のページ構造が変更されて価格やタイトルの要素が見つからなくなった場合でも、エラーで停止せずに安全に処理を終了（`None`を返す）させることができます。

- **価格の解析エラー処理**:
  取得した価格文字列（例: `"$99.99"`）から通貨記号を取り除き、`float`型に変換する処理は、予期しない形式の文字列（例: "在庫切れ"など）が来た場合に`ValueError`や`IndexError`を引き起こす可能性があります。この変換処理も`try...except`で囲むことで、価格の解析に失敗した場合でもプログラムが停止しないようにしています。

- **メール送信時のエラー**:
  `send_email_alert`関数内で、`smtplib.SMTPException`を捕捉しています。これにより、SMTP サーバーへの接続失敗、認証エラー、その他のメール送信に関する問題が発生した場合でも、エラーメッセージを表示してプログラムは続行（または終了）できます。

これらの改善により、外部サービス（Web サイトやメールサーバー）の予期せぬ変更や障害に対して、より堅牢で安定したプログラムになっています。
