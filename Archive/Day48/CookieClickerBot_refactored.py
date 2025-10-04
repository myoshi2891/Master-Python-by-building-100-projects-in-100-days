# 主な変更点は以下の通りです。
# 1.  **クラスベース設計**: 自動化のロジックを`CookieClickerBot`クラスにカプセル化し、グローバル変数をなくして状態管理を明確にします。
# 2.  **責務の分離**: 「クッキーをクリックする」「アップグレードを購入する」「ゲームを実行する」といった各機能を、クラス内の独立したメソッドに分割します。
# 3.  **コードのDRY化**: `try...except`ブロック内で重複していたアイテム購入処理を、一つのヘルパーメソッドにまとめます。
# 4.  **可読性の向上**: メソッドや変数に分かりやすい名前を付け、ロジックの流れを追いやすくします。
# 5.  **堅牢性の向上**: クッキーの数を取得する処理をより安全な方法に変更し、`int()`変換時のエラーに対応します。

# 以下がリファクタリング後の完全なコードです。

# ```python
from time import sleep, time
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class CookieClickerBot:
    """クッキークリッカーを自動でプレイするボット"""

    def __init__(self, driver_path: str):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        service = Service(driver_path, log_path="chromedriver.log")
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def open_game(self) -> None:
        """ゲームページを開き、初期設定を行う"""
        self.driver.get("https://ozh.github.io/cookieclicker/")
        self._select_language()
        self._dismiss_cookie_banner()

    def _select_language(self) -> None:
        """言語を日本語に設定する"""
        try:
            lang_select_wait = WebDriverWait(self.driver, 180)
            language_button = lang_select_wait.until(
                EC.presence_of_element_located((By.ID, "langSelect-JA"))
            )
            language_button.click()
        except TimeoutException:
            print("言語選択画面が3分以内に表示されませんでした。")
            self.quit()

    def _dismiss_cookie_banner(self) -> bool:
        """クッキーの同意バナーを閉じる"""
        try:
            consent_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cc_btn.cc_btn_accept_all"))
            )
            consent_button.click()
            return True
        except TimeoutException:
            return False

    def _buy_best_upgrade(self) -> None:
        """購入可能な最も高価なアップグレードを1つ購入する"""
        try:
            products = self.driver.find_elements(By.CSS_SELECTOR, "div.product.enabled")
            if not products:
                return

            best_item = products[-1]  # enabledなもののうち一番下のものが最も高価
            self._purchase_item(best_item)

        except NoSuchElementException:
            print("アップグレードアイテムが見つかりませんでした。")
        except Exception as e:
            print(f"アップグレード購入中に予期せぬエラーが発生しました: {e}")

    def _purchase_item(self, item: WebElement) -> None:
        """指定されたアイテムをクリックして購入し、結果をログに出力する"""
        try:
            item.click()
            product_id = item.get_attribute("id") or ""
            if product_id:
                product_name_id = product_id.replace("product", "productName")
                product_name = self.driver.find_element(By.ID, value=product_name_id).text
                print(f"購入成功: {product_name} ({product_id})")
        except ElementClickInterceptedException:
            # バナーが邪魔している場合、再度閉じてから購入を試みる
            if self._dismiss_cookie_banner():
                item.click()
                product_id = item.get_attribute("id") or ""
                if product_id:
                    product_name_id = product_id.replace("product", "productName")
                    product_name = self.driver.find_element(By.ID, value=product_name_id).text
                    print(f"バナー解消後に購入成功: {product_name} ({product_id})")
        except NoSuchElementException:
            print("購入したアイテム名の取得に失敗しました。")

    def run(self, duration_seconds: int, check_interval_seconds: int) -> None:
        """指定された時間、ゲームを自動で実行する"""
        try:
            big_cookie = self.wait.until(EC.presence_of_element_located((By.ID, "bigCookie")))
        except TimeoutException:
            print("クッキーが見つかりませんでした。ゲームが正しく読み込まれていない可能性があります。")
            self.quit()
            return

        start_time = time()
        timeout = time() + check_interval_seconds

        while time() < start_time + duration_seconds:
            sleep(0.001)  # CPU負荷を軽減
            big_cookie.click()

            if time() > timeout:
                self._buy_best_upgrade()
                timeout = time() + check_interval_seconds

        self._print_final_stats()
        self.quit()

    def _print_final_stats(self) -> None:
        """最終的なクッキーの数を表示する"""
        try:
            cookies_element = self.driver.find_element(By.ID, "cookies")
            print(f"\nゲーム終了！最終クッキー: {cookies_element.text}")
        except NoSuchElementException:
            print("最終クッキー数を取得できませんでした。")

    def quit(self) -> None:
        """ブラウザを閉じる"""
        print("ブラウザを終了します。")
        self.driver.quit()


def main():
    """スクリプトのメインエントリポイント"""
    try:
        driver_path = ChromeDriverManager().install()
        bot = CookieClickerBot(driver_path)
        bot.open_game()
        bot.run(duration_seconds=30, check_interval_seconds=10)
    except Exception as e:
        print(f"スクリプトの実行中にエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
# ```
