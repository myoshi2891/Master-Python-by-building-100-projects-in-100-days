# Instagram の「後で」ボタンを特定する方法:XPath や CSS セレクターを使用して、より堅牢な方法で要素を特定

## 推奨される方法

```python

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 方法1: テキストコンテンツで検索（最も堅牢）
try:
    later_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='後で']"))
    )
    later_button.click()
    print("「後で」ボタンをクリックしました")
except TimeoutException:
    print("「後で」ボタンが見つかりませんでした")
```

## その他の方法

```python

# 方法2: 部分的なクラス名とrole属性で検索
try:
    later_button = self.driver.find_element(
        By.XPATH,
        "//div[@role='button' and contains(@class, 'x1i10hfl') and contains(text(), '後で')]"
    )
    later_button.click()
except NoSuchElementException:
    print("「後で」ボタンが見つかりませんでした")

# 方法3: CSSセレクターを使用
try:
    later_button = self.driver.find_element(
        By.CSS_SELECTOR,
        "div[role='button'].x1i10hfl.xjqpnuy"
    )
    # テキストが「後で」であることを確認
    if "後で" in later_button.text:
        later_button.click()
except NoSuchElementException:
    print("「後で」ボタンが見つかりませんでした")
```

## あなたのコードへの統合例

```python

def login(self, username: str, password: str):
    url = URL
    self.driver.get(url)
    sleep(4.2)

    self.username = self.driver.find_element(By.NAME, value="username")
    self.username.send_keys(username)
    self.password = self.driver.find_element(By.NAME, value="password")
    self.password.send_keys(password)

    sleep(2.1)
    self.password.send_keys(Keys.ENTER)

    sleep(4.3)

    # 「ログイン情報を保存」のポップアップ処理
    try:
        # 「後で」ボタンを待機してクリック
        later_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='後で']"))
        )
        later_button.click()
        print("「後で」ボタンをクリックしました")
        sleep(2)
    except TimeoutException:
        print("「後で」ボタンが見つかりませんでした（既に処理済みの可能性）")

    # 通知のポップアップ処理（表示される場合）
    try:
        not_now_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '後で') or contains(text(), '今はしない')]"))
        )
        not_now_button.click()
        print("通知ポップアップを閉じました")
    except TimeoutException:
        print("通知ポップアップは表示されませんでした")
```

## ポイント

1. **`WebDriverWait`を使用**: 要素が表示されるまで待機し、タイミングの問題を回避
2. **テキストで検索**: クラス名は変更される可能性が高いため、テキストコンテンツで検索する方が堅牢
3. **例外処理**: ポップアップが表示されない場合もあるため、適切なエラーハンドリングを実装
4. **`role='button'`属性**: ボタン要素を特定するための追加条件として使用

この方法で、Instagram の「後で」ボタンを確実にクリックできるはずです。

この警告は、Permissions Policy による`unload`イベントの使用制限に関するものです。これはブラウザ側の警告であり、通常は Selenium の動作には影響しません。ただし、ログを整理したい場合は以下の対応方法があります。

## 対応方法

### 方法 1: Chrome オプションでログレベルを調整（推奨）

```python
# File: /Users/mitsuruyoshizumi/workspace/Python/Master-Python-by-building-100-projects-in-100-days/Day52/main.py

class InstaFollower:
    def __init__(self, followers: int):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        # コンソールログを抑制
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # より詳細な制御が必要な場合
        chrome_options.add_argument('--log-level=3')  # 0=INFO, 1=WARNING, 2=ERROR, 3=FATAL

        # Permissions Policy の警告を抑制
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.username = USERNAME
        self.password = PASSWORD
        self.followers = followers
```

### 方法 2: Service オブジェクトでログを制御

```python
# File: /Users/mitsuruyoshizumi/workspace/Python/Master-Python-by-building-100-projects-in-100-days/Day52/main.py

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class InstaFollower:
    def __init__(self, followers: int):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--log-level=3')

        # Serviceオブジェクトでログファイルを指定
        service = Service(
            ChromeDriverManager().install(),
            log_path='NUL' if os.name == 'nt' else '/dev/null'  # Windows/Unix対応
        )

        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.username = USERNAME
        self.password = PASSWORD
        self.followers = followers
```

### 方法 3: より包括的な設定

```python
# File: /Users/mitsuruyoshizumi/workspace/Python/Master-Python-by-building-100-projects-in-100-days/Day52/main.py

class InstaFollower:
    def __init__(self, followers: int):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        # ログとコンソールメッセージを抑制
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')

        # 自動化検出を回避
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Permissions Policy関連の警告を抑制
        chrome_options.add_argument('--disable-features=PermissionsPolicy')

        # その他の有用な設定
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.username = USERNAME
        self.password = PASSWORD
        self.followers = followers
```

### 方法 4: 完全なリファクタリング版（推奨）

```python
# File: /Users/mitsuruyoshizumi/workspace/Python/Master-Python-by-building-100-projects-in-100-days/Day52/main.py

from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

SIMILAR_ACCOUNT = os.getenv("SIMILAR_ACCOUNT", "")
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")
URL = os.getenv("URL", "https://google.com/")
ILLUST_URL = os.getenv("ILLUST_URL", "https://www.pixiv.net/users/illust-1134596/profile")


class InstaFollower:
    def __init__(self, followers: int):
        self.username = USERNAME
        self.password = PASSWORD
        self.followers = followers
        self.driver = self._initialize_driver()

    def _initialize_driver(self) -> webdriver.Chrome:
        """WebDriverを初期化し、適切なオプションを設定"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        # ログとコンソールメッセージを抑制
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--log-level=3')

        # 自動化検出を回避
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Permissions Policy警告を抑制
        chrome_options.add_argument('--disable-features=PermissionsPolicy')

        # Serviceオブジェクトでログを制御
        service = Service(
            ChromeDriverManager().install(),
            log_path='NUL' if os.name == 'nt' else '/dev/null'
        )

        return webdriver.Chrome(service=service, options=chrome_options)

    def login(self, username: str, password: str) -> None:
        """Instagramにログイン"""
        self.driver.get(URL)
        sleep(4.2)

        # ログイン情報を入力
        username_input = self.driver.find_element(By.NAME, value="username")
        username_input.send_keys(username)

        password_input = self.driver.find_element(By.NAME, value="password")
        password_input.send_keys(password)

        sleep(2.1)
        password_input.send_keys(Keys.ENTER)

        sleep(4.3)

        # ポップアップ処理
        self._handle_save_login_popup()
        self._handle_notification_popup()

    def _handle_save_login_popup(self) -> None:
        """「ログイン情報を保存」ポップアップを処理"""
        try:
            later_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='後で']"))
            )
            later_button.click()
            print("「後で」ボタンをクリックしました")
        except TimeoutException:
            print("「後で」ボタンが見つかりませんでした（既に処理済みの可能性）")

    def _handle_notification_popup(self) -> None:
        """通知ポップアップを処理"""
        try:
            not_now_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), '後で') or contains(text(), '今はしない')]")
                )
            )
            not_now_button.click()
            print("通知ポップアップを閉じました")
        except TimeoutException:
            print("通知ポップアップは表示されませんでした")

    def find_followers(self, target_user: str) -> None:
        """指定ユーザーのフォロワー一覧を表示"""
        self.driver.get(ILLUST_URL)
        sleep(4.2)

        try:
            follower_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'フォロワー')]"))
            )
            follower_link.click()
            sleep(2.3)
            print("フォロワー一覧に切り替えました")
        except TimeoutException:
            print("フォロワーリンクが見つかりませんでした")

    def follow(self, target_user: str) -> None:
        """指定ユーザーをフォロー"""
        # TODO: 実装予定
        pass


def main():
    """メイン処理"""
    bot = InstaFollower(0)
    try:
        bot.login(USERNAME, PASSWORD)
        bot.find_followers(target_user=SIMILAR_ACCOUNT)
        bot.follow(target_user=SIMILAR_ACCOUNT)
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
```

## 主な変更点

1. **`_initialize_driver`メソッド**: WebDriver の初期化を独立したメソッドに分離
2. **ログ抑制**: `excludeSwitches`と`log-level`でコンソールログを制御
3. **Permissions Policy 警告の抑制**: `--disable-features=PermissionsPolicy`を追加
4. **ログファイルの無効化**: Service オブジェクトでログを NULL デバイスにリダイレクト
5. **プライベートメソッド**: ポップアップ処理を`_handle_*`メソッドに分離
6. **型ヒント**: メソッドの戻り値に型ヒントを追加

これらの設定により、コンソールの警告メッセージが大幅に減少します。

## Instagram 自動フォロー修正ノート（README）

このドキュメントは、本スレッドで実施した**不具合の原因特定**と**修正内容**を、後から参照できるように要約したものです。Selenium による Instagram の操作は**自動化検知や ToS の制約**が厳しいため、技術的な修正に加えて**運用上の注意**も併記しています。

---

## 目次

1. [レート制限の**誤検出**（クリック前に即 True）](#1)
2. [`'builtin_function_or_method' object has no attribute 'time'` エラー](#2)
3. [`follow()` の**再設計**（状態遷移を待つ実装）](#3)
4. [**操作可能性プローブ**（Network ログで `/friendships/.../follow/` を確認）](#4)
5. [**セレクタ強化**と既フォロー除外のロジック](#5)
6. [**クリック無効化の主因**（オーバーレイ等）と対策](#6)
7. [**自動化検知/実レート制限**への対処と運用ルール](#7)
8. [**ログイン/環境の落とし穴**（URL・Cookie・ポップアップ）](#8)
9. [**導入チェックリスト**（適用順の確認）](#9)

---

<a id="1"></a>

## 1) レート制限の**誤検出**

### 問題点

- クリック前から `⛔ レート制限` が出る。ログ上は**0 件フォローのまま停止**。
- `_check_rate_limit()` が**ページ全体**から `"Try Again Later"` 等を `contains(text(), …)` で検索 → **ヘルプ文言/非表示要素に常在**し、誤検知。

### 修正内容

- 判定を**表示中ダイアログ内**（`role="dialog"` かつ `aria-hidden != true`）の**可視テキスト**に限定。
- クリック直後は**すぐに判定しない**。
  → **ボタン文言の変化**（`フォロー中/Following/リクエスト済み`）**または**実際の**レート制限ダイアログ出現**の**どちらか**が起きるまで**短時間ポーリング**。

#### 代表コード（抜粋）

```python
def _check_rate_limit(self, wait_seconds: float = 0) -> bool:
    import time
    deadline = time.time() + wait_seconds
    X = "//div[@role='dialog' and (not(@aria-hidden) or @aria-hidden='false')]"
    MESSAGES = ["しばらくしてからもう一度実行してください",
                "コミュニティを守るため",
                "Try Again Later", "We restrict certain activity"]
    while True:
        for dlg in self.driver.find_elements(By.XPATH, X):
            if dlg.is_displayed() and any(m in dlg.text for m in MESSAGES):
                return True
        if time.time() >= deadline: break
        sleep(0.25)
    return False
```

---

<a id="2"></a>

## 2) `'builtin_function_or_method' object has no attribute 'time'`

### 問題点2

- `time.time()` 呼び出しで上記エラー。`time` モジュール名が**別オブジェクトで上書き**されている。

### 原因

- 例：`from time import sleep` と `import time` の併用後に `time = sleep` 的な上書き／変数名衝突。

### 修正内容2

- **import を統一**し、`time` という**変数名**を使わない。
  例：

  ```python
  import time
  time.sleep(1.0)
  # もしくは
  from time import sleep
  sleep(1.0)
  ```

- デバッグ時に `print(type(time))` が `<class 'module'>` であることを確認。

---

<a id="3"></a>

## 3) `follow()` の**再設計**（状態遷移を待つ）

### 問題点

- クリック直後に `_check_rate_limit()` を即実行 → 誤検出で停止。
- `ElementClickIntercepted` 時の**再試行**や**状態遷移の待機**が不足。

### 修正内容（要点）

- **処理フロー**

  1. フォロワー**ダイアログ取得**
  2. **候補ボタン取得** → 既フォロー系文言は**即スキップ**
  3. `scrollIntoView` → `ActionChains.click` で**遮蔽対策**
  4. **状態遷移待ち**（最大 ~6s）

     - ボタン文言が `フォロー中/Following/リクエスト済み` → **成功**
     - **ダイアログ限定**でレ限文言 → **停止**
     - いずれも無 → **スキップ**

  5. 目標未達なら**軽くスクロール**して再取得

- **待機の人間化**：基礎 + 徐々に増分 + ランダムゆらぎ

> 実装はスレッドで提示済みの `follow()` に差し替え。`_wait_follow_result_or_limit()` を中核に据える。

---

<a id="4"></a>

## 4) **操作可能性プローブ**（/friendships を見る）

### 目的

- 「**Selenium のクリックが本当に API を発火しているか**」を**1 件だけ**で切り分ける。

### 修正内容

- Chrome の **Performance Log** を有効化し、直近の `Network.requestWillBeSent` から
  **`/friendships/.../(follow|unfollow|pending)`** を検出。

#### セットアップ（起動時）

```python
caps = webdriver.DesiredCapabilities.CHROME.copy()
caps["goog:loggingPrefs"] = {"performance": "ALL"}
self.driver = webdriver.Chrome(service=service, options=chrome_options,
                               desired_capabilities=caps)
```

#### 解釈

- `UI結果: followed` **かつ** `🌐 API 検出: .../friendships/.../follow/`
  → **この環境で Selenium 操作は成立**
- `UI結果: rate_limited` → **実レ限**（頻度/間隔/時間帯の見直し）
- `UI結果: unknown` **かつ** API 検出なし
  → クリック無効（**検知/オーバーレイ/ロケータずれ**）が濃厚

---

<a id="5"></a>

## 5) **セレクタ強化**と既フォロー除外

### 修正内容

- ダイアログ配下に限定し、言語とロールの揺れを吸収する XPath：

```xpath
.//*[self::button or @role='button']
   [normalize-space(text())='フォロー' or normalize-space(text())='Follow'
    or @aria-label='フォローする']
```

- **既状態の除外**：

  - `{"フォロー済み","フォロー中","リクエスト済み","ブロック済み","Following","Requested"}` は**スキップ**。

---

<a id="6"></a>

## 6) クリック無効化（オーバーレイ等）と対策

### 症状

- `ElementClickInterceptedException`、あるいは**クリックしても何も起きない**。

### 修正内容

- クリック前に **中央へスクロール**＋**`ActionChains.move_to_element`**。
- 位置に**何が載っているか**をヒットテスト：

```python
# ボタンの中心座標で elementFromPoint を確認
overlay = self.driver.execute_script(
  "return document.elementFromPoint(arguments[0], arguments[1]);", x, y
)
print("overlay tag:", overlay.tag_name)
# ボタン以外なら、被っている要素（トースト/バナー/tooltip）を閉じる
```

- `_handle_follow_dialog()` で **OK/Close** を潰して再クリック。

---

<a id="7"></a>

## 7) 自動化検知/実レート制限の対処と運用

### 推奨運用

- **ヘッドレスは避ける**、**User-Agent 明示**、**ゆらぎのある待機**（3.2–6.8s）
- **1 セッションあたりのフォロー数を小さく**（数十件以下）
- **undetected-chromedriver / Playwright+stealth** の検討（リスク理解の上で）

> ⚠️ **重要**：自動化はプラットフォームの**利用規約に抵触する可能性**があります。
> アカウント停止等のリスクを理解し、自己責任で運用してください。

---

<a id="8"></a>

## 8) ログイン/環境の落とし穴（URL・Cookie・ポップアップ）

### 問題点と修正

- `.env` の `ILLUST_URL` が **Pixiv デフォルト** → Instagram プロフ URL を必ず指定。
- ログイン直後の **「後で/今はしない」** ポップアップを確実に閉じる（`authorized` 後の UI を安定化）。
- **`csrftoken`** が Cookie に存在するか確認（セッション確立待ちを十分に）。

---

<a id="9"></a>

## 9) 導入チェックリスト（適用順）

1. **import 衝突**解消：`time` はモジュールのまま（`time.time()` が動く）。
2. `ILLUST_URL` を **Instagram プロフ URL** に設定。
3. ログイン後の **ポップアップ閉じ**が成功している。
4. `follow()` を**状態遷移待ち版**に差し替え（誤判定の `_check_rate_limit()` 即時呼び出しを撤廃）。
5. セレクタを**ダイアログ配下**＋**多言語/role**に対応。
6. クリック前の **`scrollIntoView` + `ActionChains`**、遮蔽時は **`_handle_follow_dialog()`**。
7. **操作可能性プローブ**で `/friendships/.../follow/` が検出されるか確認。
8. 実レ限が出たら**頻度/待機/時間帯**を調整（セッション分割）。

---

## Day52 Instagram Bot リファクタリング記録

## 修正概要

Instagram の自動フォローボットにおいて、レート制限への対応と堅牢性の向上を実施しました。

---

## 主な修正項目

### 1. レート制限検出の改善

**問題点:**

- レート制限ダイアログの検出が不安定
- ページ全体を検索するため、無関係な要素を誤検出
- 検出タイミングが遅く、無駄なフォロー試行が発生

**修正内容:**

```python
def _check_rate_limit(self, wait_seconds: float = 0) -> bool:
    """表示中のダイアログ内に限定してレート制限メッセージを確認"""
    # 可視状態のダイアログのみを対象
    XPATH_DIALOG = "//div[@role='dialog' and (not(@aria-hidden) or @aria-hidden='false')]"

    # 複数言語のメッセージに対応
    MESSAGES = [
        "しばらくしてからもう一度実行してください",
        "コミュニティを守るため",
        "Try Again Later",
        "We restrict certain activity",
    ]
```

**効果:**

- 誤検出の削減
- レート制限の即座な検出
- 多言語環境への対応

---

### 2. フォロー結果の状態遷移監視

**問題点:**

- クリック後の成功/失敗判定が曖昧
- ボタンの状態変化を確認せずに次の処理へ進行
- レート制限発生時の検出遅延

**修正内容:**

```python
def _wait_follow_result_or_limit(self, button, timeout: float = 6.0) -> str:
    """
    クリック後の結果を待機:
    - ボタン文言が変化 → "followed"
    - レート制限検出 → "rate_limited"
    - 変化なし → "unknown"
    """
    TARGETS = {"フォロー中", "Following", "リクエスト済み", "Requested"}

    while time.time() < end:
        if button.text.strip() in TARGETS:
            return "followed"
        if self._check_rate_limit():
            return "rate_limited"
        time.sleep(0.25)
```

**効果:**

- フォロー成功の確実な確認
- レート制限の即座な検出と処理中断
- 無駄な API 呼び出しの削減

---

### 3. 要素の可視性チェック強化

**問題点:**

- 非表示要素へのアクセスでエラー発生
- `is_displayed()`呼び出し時の例外処理不足

**修正内容:**

```python
def _is_visible(self, el) -> bool:
    """要素の可視性を安全にチェック"""
    try:
        return el.is_displayed()
    except Exception:
        return False
```

**効果:**

- 例外による処理中断の防止
- より安定した要素検出

---

### 4. フォロー処理のフロー改善

**問題点:**

- レート制限後も処理を継続
- 無限ループのリスク
- 進捗状況が不明瞭

**修正内容:**

```python
def follow(self, max_follows: int = 50) -> None:
    """改善されたフォロー処理"""
    followed_count = 0
    skipped_count = 0
    error_count = 0

    while followed_count < max_follows:
        # レート制限チェック
        if self.rate_limited:
            print(f"\n⛔ レート制限により処理中断（{followed_count}人フォロー後）")
            self._print_summary(followed_count, skipped_count, error_count)
            return

        # フォロー実行
        result = self._wait_follow_result_or_limit(button, timeout=6.0)

        if result == "rate_limited":
            self.rate_limited = True
            return
        elif result == "followed":
            followed_count += 1
            # 人間らしい待機時間
            time.sleep(base_wait + step_wait + jitter)
```

**効果:**

- レート制限時の即座な処理停止
- 詳細な進捗表示
- 統計情報の記録

---

### 5. エラーハンドリングの強化

**問題点:**

- 例外発生時の情報不足
- 処理継続可否の判断が困難

**修正内容:**

```python
try:
    # フォロー処理
    pass
except TimeoutException:
    print("❌ フォロワーポップアップが見つかりませんでした")
except Exception as e:
    print(f"❌ フォロー処理で予期せぬエラー: {e}")
    import traceback
    traceback.print_exc()
```

**効果:**

- 詳細なエラー情報の出力
- デバッグの容易化
- 問題箇所の特定が迅速化

---

### 6. 人間らしい動作の実装

**問題点:**

- 一定間隔での機械的なクリック
- Bot 検出のリスク増加

**修正内容:**

```python
# 段階的に待機時間を増加
base_wait = 3.5
step_wait = min(idx * 0.25, 4.0)  # 最大4秒まで増加
jitter = random.uniform(0.15, 0.6)  # ランダムなゆらぎ
time.sleep(base_wait + step_wait + jitter)
```

**効果:**

- より自然な動作パターン
- Bot 検出リスクの低減
- アカウント制限の回避

---

## 技術的改善点

### コードの保守性向上

- 責務の明確な分離（検出・判定・実行）
- 定数の適切な管理
- 型ヒントの追加

### パフォーマンス最適化

- 不要な待機時間の削減
- 効率的な要素検索
- リトライロジックの最適化

### ログ出力の改善

- 絵文字による視認性向上
- 詳細な進捗情報
- エラー時のスタックトレース

---

## 今後の改善案

1. **設定の外部化**: 待機時間やメッセージを設定ファイルで管理
2. **統計情報の永続化**: フォロー履歴をデータベースに保存
3. **リトライ戦略**: 一時的なエラーに対する自動リトライ
4. **通知機能**: レート制限時のメール/Slack 通知
5. **テストの追加**: ユニットテストと E2E テストの実装

---
