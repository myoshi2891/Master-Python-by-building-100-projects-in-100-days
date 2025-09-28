# 主な変更点は以下の通りです。

# 1.  **クラスベース設計**: スクレイピングのロジックを`PythonOrgScraper`クラスにカプセル化し、責務を明確にします。
# 2.  **責務の分離**: 「ブラウザの初期化」「イベント情報の取得」「ブラウザの終了」といった各機能を、独立したメソッドに分割します。
# 3.  **堅牢性の向上**:
#     *   `try...finally`ブロックを導入し、処理中にエラーが発生してもブラウザが確実に終了するようにします。
#     *   `WebDriverWait`を使用して、要素が表示されるまで待機し、スクリプトの安定性を高めます。
# 4.  **データ抽出ロジックの改善**: イベントの日時と名前をより安全にペアリングするために、`zip`関数を使用します。これにより、リストの要素数がずれた場合にエラーを防ぎやすくなります。
# 5.  **コードのクリーンアップ**: 不要なコメントアウトされたコードを削除し、可読性を向上させます。
# 6.  **エントリーポイントの明確化**: `if __name__ == "__main__":`ブロックを使い、スクリプトとして直接実行される処理を`main`関数にまとめます。

# 以下がリファクタリング後のコードです。

# ```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class PythonOrgScraper:
    """python.orgからイベント情報を取得するスクレイパークラス"""

    def __init__(self):
        """WebDriverを初期化する"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)

    def get_upcoming_events(self, url: str) -> dict:
        """指定されたURLから近々のイベント情報を取得する"""
        self.driver.get(url)

        # イベントウィジェットが読み込まれるまで待機
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".event-widget")))

        event_times = self.driver.find_elements(By.CSS_SELECTOR, value=".event-widget time")
        event_names = self.driver.find_elements(By.CSS_SELECTOR, value=".event-widget li a")

        events = {}
        # zipを使って時間と名前を安全に組み合わせる
        for i, (time, name) in enumerate(zip(event_times, event_names)):
            events[i] = {
                "time": time.text,
                "name": name.text,
            }
        return events

    def close_browser(self):
        """ブラウザを閉じる"""
        self.driver.quit()


def main():
    """スクリプトのメイン処理"""
    scraper = PythonOrgScraper()
    try:
        events = scraper.get_upcoming_events("https://www.python.org/")
        print("Upcoming Events on python.org:")
        print(events)
    except Exception as e:
        print(f"An error occurred: {e}")
    # 'detach'オプションが有効なため、ブラウザは自動で閉じません。
    # 処理完了後に自動で閉じたい場合は、以下のfinallyブロックのコメントを解除してください。
    # finally:
    #     print("\nClosing browser...")
    #     scraper.close_browser()


if __name__ == "__main__":
    main()
# ```
