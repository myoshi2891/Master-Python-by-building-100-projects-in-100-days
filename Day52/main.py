import os
import random
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

SIMILAR_ACCOUNT = os.getenv("SIMILAR_ACCOUNT", "")
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")
URL = os.getenv("URL", "https://google.com/")
ILLUST_URL = os.getenv(
    "ILLUST_URL", "https://www.pixiv.net/users/illust-1134596/profile"
)


class InstaFollower:
    def __init__(self, followers: int):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        # ログとコンソールメッセージを抑制
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--log-level=3")

        # 自動化検出を回避
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Permissions Policy警告を抑制
        chrome_options.add_argument("--disable-features=PermissionsPolicy")

        # Serviceオブジェクトでログを制御
        service = Service(
            ChromeDriverManager().install(),
            log_path="NUL" if os.name == "nt" else "/dev/null",
        )
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        self.username = USERNAME
        self.password = PASSWORD
        self.followers = followers
        self.rate_limited = False  # レート制限フラグ

    def login(self, username: str, password: str):
        url = URL
        self.driver.get(url)
        time.sleep(4.2)

        # # Check if the cookie warning is present on the page
        # decline_cookies_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]"
        # cookie_warning = self.driver.find_elements(By.XPATH, decline_cookies_xpath)
        # if cookie_warning:
        #     # Dismiss the cookie warning by clicking an element or button
        #     cookie_warning[0].click()

        self.username = self.driver.find_element(By.NAME, value="username")
        self.username.send_keys(username)
        self.password = self.driver.find_element(By.NAME, value="password")
        self.password.send_keys(password)

        time.sleep(2.1)
        self.password.send_keys(Keys.ENTER)

        time.sleep(4.3)
        try:
            later_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@role='button' and text()='後で']")
                )
            )
            later_button.click()
            print("「後で」ボタンをクリックしました")
        except TimeoutException:
            print("「後で」ボタンが見つかりませんでした")

        try:
            not_now_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(text(), '後で') or contains(text(), '今はしない')]",
                    )
                )
            )
            not_now_button.click()
            print("通知ポップアップを閉じました")
        except TimeoutException:
            print("通知ポップアップは表示されませんでした")

    def follow(self, max_follows: int = 50) -> None:
        """
        フォロワー一覧ポップアップ内の 'フォロー' ボタンを順にクリックし、
        クリック後の状態遷移（フォロー成功 or レート制限）を観測して制御する。
        """
        print(f"\n🎯 フォロー処理を開始します（最大{max_follows}人）\n")

        try:
            # 1) フォロワーのポップアップを待機
            popup = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )
            print("ポップアップを検出")

            followed_count = 0
            skipped_count = 0
            error_count = 0

            # 2) 目標数に達するまで繰り返し
            attempts = 0
            max_attempts = max(
                4, max_follows * 2
            )  # ボタン再取得の回数上限（適度に余裕）
            while (followed_count < max_follows) and (attempts < max_attempts):
                attempts += 1

                # 3) 今見えているフォローボタンを取得
                follow_buttons = self._find_follow_buttons(popup)
                if not follow_buttons:
                    print(f"\n⚠️  フォローボタンが見つかりません（試行 {attempts}）")
                    time.sleep(1.0)
                    # 画面に変化を与えるため軽くスクロール
                    self._scroll_popup_slightly(popup)
                    continue

                print(f"\n📋 {len(follow_buttons)}個のフォローボタンを検出")

                # 4) ボタンを順次処理
                for idx, button in enumerate(follow_buttons):
                    if followed_count >= max_follows:
                        break

                    try:
                        if not button.is_enabled():
                            continue

                        label = (button.text or "").strip()
                        if label in {
                            "フォロー済み",
                            "フォロー中",
                            "ブロック済み",
                            "リクエスト済み",
                            "Following",
                            "Requested",
                        }:
                            skipped_count += 1
                            print(
                                f"[{idx + 1}/{len(follow_buttons)}] 既状態({label})のためスキップ"
                            )
                            continue

                        username = self._get_username_from_button(button)

                        # 4-1) クリック前の可視化・位置調整
                        try:
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({block:'center'});", button
                            )
                            time.sleep(1)
                        except Exception:
                            pass

                        # 4-2) クリック（遮蔽対策として ActionChains 経由）
                        try:
                            ActionChains(self.driver).move_to_element(button).pause(
                                0.05
                            ).click(button).perform()
                        except ElementClickInterceptedException:
                            print(
                                "   ⚠️  クリックがブロックされました。ダイアログを確認中..."
                            )
                            if self._handle_follow_dialog():
                                print("   ℹ️  ダイアログを処理しました。続行します。")
                                # ダイアログを閉じたので、同じボタンをもう一度試す
                                try:
                                    ActionChains(self.driver).move_to_element(
                                        button
                                    ).pause(0.05).click(button).perform()
                                except Exception as e2:
                                    error_count += 1
                                    print(f"   ❌ 再クリック失敗: {e2}")
                                    continue
                            else:
                                error_count += 1
                                continue

                        # 4-3) クリック後の状態遷移を観測
                        result = self._wait_follow_result_or_limit(button, timeout=6.0)
                        if result == "rate_limited":
                            self.rate_limited = True
                            print(
                                f"\n⛔ レート制限を検出しました（{followed_count}人フォロー後）"
                            )
                            # サマリを出して終了
                            print(
                                f"\n📊 結果: followed={followed_count}, skipped={skipped_count}, errors={error_count}"
                            )
                            return
                        elif result == "followed":
                            followed_count += 1
                            print(
                                f"[{idx + 1}/{len(follow_buttons)}] {username} をフォローしました"
                            )

                            # 4-4) 人間らしい待機（少しずつ伸ばす＋ランダムゆらぎ）
                            base_wait = 3.5
                            step_wait = min(idx * 0.25, 4.0)
                            jitter = random.uniform(0.15, 0.6)
                            time.sleep(base_wait + step_wait + jitter)

                        else:  # "unknown"
                            skipped_count += 1
                            print(
                                f"[{idx + 1}/{len(follow_buttons)}] 状態遷移が確認できずスキップ"
                            )

                    except Exception as e:
                        error_count += 1
                        print(f"   ❌ エラー: {e}")
                        continue

                # 5) まだ目標未達 & レ限で止まっていない → 少しスクロールして再取得
                if (followed_count < max_follows) and (not self.rate_limited):
                    self._scroll_popup_slightly(popup)
                    time.sleep(1.2)

            # 6) 終了サマリ
            if followed_count >= max_follows:
                print(f"\n🎉 目標の {max_follows} 人をフォローしました")
            print(
                f"\n📊 結果: followed={followed_count}, skipped={skipped_count}, errors={error_count}"
            )

        except TimeoutException:
            print("❌ フォロワーポップアップが見つかりませんでした")
        except Exception as e:
            print(f"❌ フォロー処理で予期せぬエラー: {e}")
            import traceback

            traceback.print_exc()

    def _is_visible(self, el) -> bool:
        try:
            return el.is_displayed()
        except Exception:
            return False

    def _check_rate_limit(self, wait_seconds: float = 0) -> bool:
        """
        '表示中のダイアログ内' に限定して、明示的なレート制限メッセージを確認する。
        wait_seconds > 0 の場合は、その秒数だけリトライしながら監視する。
        """
        import time

        deadline = time.time() + wait_seconds
        XPATH_DIALOG = (
            "//div[@role='dialog' and (not(@aria-hidden) or @aria-hidden='false')]"
        )
        MESSAGES = [
            "しばらくしてからもう一度実行してください",
            "コミュニティを守るため",
            "Try Again Later",
            "We restrict certain activity",
        ]
        while True:
            try:
                dialogs = self.driver.find_elements(By.XPATH, XPATH_DIALOG)
                for dlg in dialogs:
                    if not self._is_visible(dlg):
                        continue
                    text = dlg.text  # 可視テキストのみ
                    for m in MESSAGES:
                        if m in text:
                            return True
            except Exception:
                pass
            if time.time() >= deadline:
                break
            time.sleep(0.25)
        return False

    def _wait_follow_result_or_limit(self, button, timeout: float = 6.0) -> str:
        """
        クリック後の結果を待つ:
        - ボタン文言がフォロー状態に変わる  -> "followed"
        - レート制限ダイアログが出る       -> "rate_limited"
        - 何も起きない/失敗                -> "unknown"
        """
        end = time.time() + timeout
        TARGETS = {"フォロー中", "Following", "リクエスト済み", "Requested"}
        last_text = ""
        while time.time() < end:
            try:
                # ボタンはDOM再構築で参照切れになる可能性があるので、親から再取得できるとより堅牢
                curr = button.text.strip()
                last_text = curr or last_text
                if curr in TARGETS:
                    return "followed"
            except Exception:
                pass
            if self._check_rate_limit():
                return "rate_limited"
            time.sleep(0.25)
        return "unknown"

    # def _check_rate_limit(self) -> bool:
    #     """レート制限ダイアログの存在をチェック"""
    #     try:
    #         # レート制限メッセージを探す
    #         rate_limit_messages = [
    #             "しばらくしてからもう一度実行してください",
    #             "Try Again Later",
    #             "コミュニティを守るため",
    #             "We restrict certain activity",
    #         ]

    #         for message in rate_limit_messages:
    #             try:
    #                 element = self.driver.find_element(
    #                     By.XPATH, f"//*[contains(text(), '{message}')]"
    #                 )
    #                 if element.is_displayed():
    #                     return True
    #             except NoSuchElementException:
    #                 continue

    #         return False
    #     except Exception:
    #         return False

    def _find_follow_buttons(self, popup):
        """ポップアップ内のフォローボタンを複数の方法で検索"""

        # 方法1: aria-labelで検索（日本語）
        try:
            buttons = popup.find_elements(
                By.CSS_SELECTOR, "button[aria-label='フォローする']"
            )
            if buttons:
                print(
                    f"   🔍 方法1で{len(buttons)}個のボタンを発見（aria-label='フォローする'）"
                )
                return buttons
        except:
            pass

        # 方法2: テキストで検索
        try:
            buttons = popup.find_elements(
                By.XPATH,
                ".//button[contains(text(), 'フォロー') and not(contains(text(), 'フォロー中'))]",
            )
            if buttons:
                print(
                    f"   🔍 方法2で{len(buttons)}個のボタンを発見（テキスト='フォロー'）"
                )
                return buttons
        except:
            pass

        # 方法3: 英語版
        try:
            buttons = popup.find_elements(By.XPATH, ".//button[text()='Follow']")
            if buttons:
                print(
                    f"   🔍 方法3で{len(buttons)}個のボタンを発見（テキスト='Follow'）"
                )
                return buttons
        except:
            pass

        # 方法4: すべてのボタンから「フォロー」を含むものを抽出
        try:
            all_buttons = popup.find_elements(By.TAG_NAME, "button")
            follow_buttons = [
                btn
                for btn in all_buttons
                if btn.text in ["フォロー", "Follow"] and btn.is_displayed()
            ]
            if follow_buttons:
                print(
                    f"   🔍 方法4で{len(follow_buttons)}個のボタンを発見（全ボタンから抽出）"
                )
                return follow_buttons
        except:
            pass

        return []

    def _handle_follow_dialog(self) -> bool:
        """フォロー制限などのダイアログを処理"""
        try:
            # 「OK」ボタンを探す
            ok_button = self.driver.find_element(
                By.XPATH, "//button[text()='OK' or text()='わかりました']"
            )
            ok_button.click()
            time.sleep(1)
            return True
        except NoSuchElementException:
            pass

        try:
            # 「閉じる」ボタンを探す
            close_button = self.driver.find_element(
                By.XPATH, "//button[text()='閉じる' or text()='Close']"
            )
            close_button.click()
            time.sleep(1)
            return True
        except NoSuchElementException:
            pass

        return False

    def _scroll_popup_slightly(self, popup) -> None:
        """ポップアップを少しだけスクロールして新しいユーザーを表示"""
        try:
            scrollable_element = self._find_scrollable_element(popup)
            if scrollable_element:
                self.driver.execute_script(
                    "arguments[0].scrollTop += 300", scrollable_element
                )
        except Exception as e:
            print(f"   ⚠️  スクロール中にエラー: {e}")

    def _get_username_from_button(self, button):
        """フォローボタンから対象ユーザー名を取得"""
        try:
            # ボタンの親要素からユーザー名を探す
            parent = button.find_element(
                By.XPATH, "./ancestor::div[contains(@class, 'x1dm5mii')]"
            )
            username_element = parent.find_element(By.TAG_NAME, "span")
            return username_element.text
        except:
            return "不明なユーザー"

    def find_followers(self, url: str):
        self.driver.get(url)
        time.sleep(4.2)
        try:
            follower_link = self.driver.find_element(
                By.CSS_SELECTOR, "a[href*='/followers/']"
            )
            follower_link.click()
            time.sleep(5.3)

            # ポップアップをスクロール
            self._scroll_follower_popup()
        except NoSuchElementException:
            pass

    def _scroll_follower_popup(
        self, scroll_count: int = 10, scroll_pause: float = 2.5
    ) -> None:
        """フォロワーリストのポップアップをスクロール"""
        try:
            # ポップアップのダイアログを待機
            popup = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )
            print("フォロワーリストのポップアップを検出")

            # スクロール可能な要素を複数の方法で探す
            scrollable_element = self._find_scrollable_element(popup)

            if not scrollable_element:
                print("❌ スクロール可能な要素が見つかりませんでした")
                return

            # スクロール前の高さを確認
            initial_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", scrollable_element
            )
            print(f"初期スクロール高さ: {initial_height}px")

            # ゆっくりスクロール実行
            last_height = initial_height
            no_change_count = 0

            # スクロール実行
            print(f"フォロワーリストを{scroll_count}回スクロールします...")

            for i in range(scroll_count):
                # 現在のスクロール位置を取得
                current_scroll = self.driver.execute_script(
                    "return arguments[0].scrollTop", scrollable_element
                )

                # スクロール実行
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight",
                    scrollable_element,
                )

                # 段階的にスクロール（一気に最下部まで行かず、少しずつスクロール）
                scroll_step = 300  # 300pxずつスクロール
                new_scroll_position = current_scroll + scroll_step

                # スクロール実行（段階的）
                self.driver.execute_script(
                    f"arguments[0].scrollTop = {new_scroll_position}",
                    scrollable_element,
                )

                # スクロール後の待機（コンテンツの読み込みを待つ）
                time.sleep(scroll_pause)

                # スクロール後の位置を確認
                new_scroll = self.driver.execute_script(
                    "return arguments[0].scrollTop", scrollable_element
                )

                # 新しいコンテンツの高さを確認
                new_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight", scrollable_element
                )

                # 進捗表示
                print(f"📍 スクロール {i + 1}/{scroll_count}")
                print(f"   位置: {current_scroll}px → {new_scroll}px")
                print(f"   高さ: {last_height}px → {new_height}px")

                print(
                    f"スクロール {i + 1}/{scroll_count} - "
                    f"位置: {current_scroll}px → {new_scroll}px, "
                    f"高さ: {new_height}px"
                )

                # スクロールが実際に動いたか確認
                if new_scroll == current_scroll and i > 0:
                    print("⚠️ これ以上スクロールできません（最下部に到達）")
                    break

            print("✅ スクロール完了")

        except TimeoutException:
            print("❌ ポップアップが見つかりませんでした")
        except Exception as e:
            print(f"❌ スクロール中にエラーが発生しました: {e}")
            import traceback

            traceback.print_exc()

    def _find_scrollable_element(self, popup):
        """スクロール可能な要素を複数の方法で探す"""

        # 方法3: ポップアップ内のすべてのdivを調べる
        try:
            all_divs = popup.find_elements(By.TAG_NAME, "div")
            print(f"ポップアップ内のdiv要素数: {len(all_divs)}")

            for idx, div in enumerate(all_divs):
                try:
                    scroll_height = self.driver.execute_script(
                        "return arguments[0].scrollHeight", div
                    )
                    client_height = self.driver.execute_script(
                        "return arguments[0].clientHeight", div
                    )

                    # スクロール可能な要素を見つけた
                    if scroll_height > client_height and client_height > 100:
                        print(f"✅ 方法3でスクロール要素を発見（div #{idx}）")
                        print(
                            f"   scrollHeight: {scroll_height}px, clientHeight: {client_height}px"
                        )
                        return div
                except:
                    print(
                        f"方法3でスクロール可能な要素を発見できませんでした（div #{idx}）"
                    )
                    continue

        except Exception as e:
            print(f"方法3でエラー: {e}")


bot = InstaFollower(0)
bot.login(USERNAME, PASSWORD)
bot.find_followers(url=ILLUST_URL)
bot.follow()
