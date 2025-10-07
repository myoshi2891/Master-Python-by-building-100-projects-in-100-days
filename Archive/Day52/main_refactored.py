from __future__ import annotations

import os
import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import Final, List, Optional, Sequence, Tuple

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
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

LOGIN_URL: Final[str] = os.getenv("URL", "https://www.instagram.com/accounts/login/")
TARGET_PROFILE_URL: Final[str] = os.getenv(
    "ILLUST_URL", "https://www.pixiv.net/users/illust-1134596/profile"
)
SIMILAR_ACCOUNT: Final[str] = os.getenv("SIMILAR_ACCOUNT", "")
USERNAME: Final[str] = os.getenv("USERNAME", "")
PASSWORD: Final[str] = os.getenv("PASSWORD", "")
DEFAULT_MAX_FOLLOWS: Final[int] = 50
MAX_POPUP_WAIT_SECONDS: Final[int] = 10
FOLLOW_DELAY_BASE_SECONDS: Final[float] = 3.5
FOLLOW_DELAY_STEP_SECONDS: Final[float] = 0.25
FOLLOW_DELAY_STEP_CAP_SECONDS: Final[float] = 4.0
FOLLOW_DELAY_JITTER_RANGE: Final[Tuple[float, float]] = (0.15, 0.6)
FOLLOW_BUTTON_QUERIES: Final[Sequence[Tuple[str, str]]] = (
    (By.CSS_SELECTOR, "button[aria-label='フォローする']"),
    (
        By.XPATH,
        ".//button[contains(text(), 'フォロー') and not(contains(text(), 'フォロー中'))]",
    ),
    (By.XPATH, ".//button[text()='Follow']"),
)
FOLLOW_SKIP_LABELS: Final[frozenset[str]] = frozenset(
    {
        "フォロー済み",
        "フォロー中",
        "ブロック済み",
        "リクエスト済み",
        "Following",
        "Requested",
    }
)
FOLLOW_SUCCESS_LABELS: Final[frozenset[str]] = frozenset(
    {"フォロー中", "Following", "リクエスト済み", "Requested"}
)
RATE_LIMIT_MESSAGES: Final[Tuple[str, ...]] = (
    "しばらくしてからもう一度実行してください",
    "コミュニティを守るため",
    "Try Again Later",
    "We restrict certain activity",
)
SCROLL_STEP_PX: Final[int] = 300
DEFAULT_SCROLL_COUNT: Final[int] = 10
DEFAULT_SCROLL_PAUSE_SECONDS: Final[float] = 2.5


class FollowStatus(Enum):
    FOLLOWED = "followed"
    RATE_LIMITED = "rate_limited"
    SKIPPED = "skipped"
    UNKNOWN = "unknown"
    ERROR = "error"


@dataclass(frozen=True)
class FollowAttempt:
    status: FollowStatus
    username: Optional[str] = None
    detail: Optional[str] = None


@dataclass(frozen=True)
class InstagramCredentials:
    username: str
    password: str


class InstaFollower:
    def __init__(
        self,
        credentials: InstagramCredentials,
        driver: Optional[WebDriver] = None,
    ) -> None:
        self.credentials = credentials
        self.driver: WebDriver = driver or self._create_driver()
        self.rate_limited = False

    def __enter__(self) -> "InstaFollower":
        return self

    def __exit__(self, exc_type, exc, exc_tb) -> bool:
        self.close()
        return False

    def close(self) -> None:
        if self.driver:
            self.driver.quit()

    def login(self) -> None:
        self.driver.get(LOGIN_URL)
        time.sleep(4.0)

        username_input = self.driver.find_element(By.NAME, value="username")
        username_input.send_keys(self.credentials.username)

        password_input = self.driver.find_element(By.NAME, value="password")
        password_input.send_keys(self.credentials.password)
        time.sleep(2.0)
        password_input.send_keys(Keys.ENTER)

        time.sleep(4.0)
        self._dismiss_save_login_popup()
        self._dismiss_notification_popup()

    def follow(self, max_follows: int = DEFAULT_MAX_FOLLOWS) -> None:
        print(f"\n🎯 フォロー処理を開始します（最大{max_follows}人）\n")

        try:
            popup = WebDriverWait(self.driver, MAX_POPUP_WAIT_SECONDS).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )
        except TimeoutException:
            print("❌ フォロワーポップアップが見つかりませんでした")
            return

        print("ポップアップを検出")
        followed_count = 0
        skipped_count = 0
        error_count = 0
        attempts = 0
        max_attempts = max(4, max_follows * 2)

        while followed_count < max_follows and attempts < max_attempts:
            attempts += 1
            follow_buttons = self._find_follow_buttons(popup)
            if not follow_buttons:
                print(f"\n⚠️  フォローボタンが見つかりません（試行 {attempts}）")
                time.sleep(1.0)
                self._scroll_popup_slightly(popup)
                continue

            print(f"\n📋 {len(follow_buttons)}個のフォローボタンを検出")
            for index, button in enumerate(follow_buttons, start=1):
                if followed_count >= max_follows:
                    break

                attempt = self._process_follow_button(button, index, len(follow_buttons))

                if attempt.status is FollowStatus.FOLLOWED:
                    followed_count += 1
                    label = attempt.username or "不明なユーザー"
                    print(f"[{index}/{len(follow_buttons)}] {label} をフォローしました")
                elif attempt.status is FollowStatus.SKIPPED:
                    skipped_count += 1
                    reason = attempt.detail or "状態遷移が確認できずスキップ"
                    print(f"[{index}/{len(follow_buttons)}] {reason}")
                elif attempt.status is FollowStatus.RATE_LIMITED:
                    self.rate_limited = True
                    print(
                        f"\n⛔ レート制限を検出しました（{followed_count}人フォロー後）"
                    )
                    print(
                        f"\n📊 結果: followed={followed_count}, skipped={skipped_count}, errors={error_count}"
                    )
                    return
                elif attempt.status is FollowStatus.ERROR:
                    error_count += 1
                    print(f"   ❌ エラー: {attempt.detail}")
                else:  # UNKNOWN
                    skipped_count += 1
                    print(
                        f"[{index}/{len(follow_buttons)}] 状態遷移が確認できずスキップ"
                    )

            if followed_count < max_follows and not self.rate_limited:
                self._scroll_popup_slightly(popup)
                time.sleep(1.2)

        if followed_count >= max_follows:
            print(f"\n🎉 目標の {max_follows} 人をフォローしました")
        print(
            f"\n📊 結果: followed={followed_count}, skipped={skipped_count}, errors={error_count}"
        )

    def _process_follow_button(
        self,
        button: WebElement,
        index: int,
        total: int,
    ) -> FollowAttempt:
        if not button.is_enabled():
            return FollowAttempt(FollowStatus.SKIPPED, detail="ボタンが無効のためスキップ")

        label = (button.text or "").strip()
        if label in FOLLOW_SKIP_LABELS:
            return FollowAttempt(
                FollowStatus.SKIPPED, detail=f"既状態({label})のためスキップ"
            )

        username = self._get_username_from_button(button)
        self._focus_button(button)

        if not self._click_follow_button(button):
            return FollowAttempt(FollowStatus.ERROR, username, "クリックに失敗")

        result = self._wait_follow_result_or_limit(button, timeout=6.0)
        if result is FollowStatus.RATE_LIMITED:
            return FollowAttempt(FollowStatus.RATE_LIMITED, username)
        if result is FollowStatus.FOLLOWED:
            self._sleep_after_follow(index)
            return FollowAttempt(FollowStatus.FOLLOWED, username)
        return FollowAttempt(FollowStatus.UNKNOWN, username)

    def _wait_follow_result_or_limit(
        self,
        button: WebElement,
        timeout: float = 6.0,
    ) -> FollowStatus:
        end = time.time() + timeout
        last_text = ""
        while time.time() < end:
            try:
                current_label = (button.text or "").strip()
                if current_label:
                    last_text = current_label
                if current_label in FOLLOW_SUCCESS_LABELS:
                    return FollowStatus.FOLLOWED
            except Exception:
                pass

            if self._check_rate_limit():
                return FollowStatus.RATE_LIMITED
            time.sleep(0.25)
        if last_text in FOLLOW_SUCCESS_LABELS:
            return FollowStatus.FOLLOWED
        return FollowStatus.UNKNOWN

    def _click_follow_button(self, button: WebElement) -> bool:
        try:
            ActionChains(self.driver).move_to_element(button).pause(0.05).click(button).perform()
            return True
        except ElementClickInterceptedException:
            print("   ⚠️  クリックがブロックされました。ダイアログを処理します。")
            if self._handle_follow_dialog():
                try:
                    ActionChains(self.driver).move_to_element(button).pause(0.05).click(button).perform()
                    return True
                except Exception as exc:
                    print(f"   ❌ 再クリックに失敗しました: {exc}")
                    return False
            return False
        except Exception as exc:
            print(f"   ❌ フォローボタンクリック時に例外が発生: {exc}")
            return False

    def _focus_button(self, button: WebElement) -> None:
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                button,
            )
            time.sleep(0.8)
        except Exception:
            pass

    def _sleep_after_follow(self, index: int) -> None:
        step_wait = min(index * FOLLOW_DELAY_STEP_SECONDS, FOLLOW_DELAY_STEP_CAP_SECONDS)
        jitter = random.uniform(*FOLLOW_DELAY_JITTER_RANGE)
        time.sleep(FOLLOW_DELAY_BASE_SECONDS + step_wait + jitter)

    def find_followers(self, url: str = TARGET_PROFILE_URL) -> None:
        self.driver.get(url)
        time.sleep(4.0)
        try:
            follower_link = self.driver.find_element(
                By.CSS_SELECTOR, "a[href*='/followers/']"
            )
            follower_link.click()
            time.sleep(5.0)
            self._scroll_follower_popup()
        except NoSuchElementException:
            print("フォロワーリンクが見つかりませんでした")

    def _scroll_follower_popup(
        self,
        scroll_count: int = DEFAULT_SCROLL_COUNT,
        scroll_pause: float = DEFAULT_SCROLL_PAUSE_SECONDS,
    ) -> None:
        try:
            popup = WebDriverWait(self.driver, MAX_POPUP_WAIT_SECONDS).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )
        except TimeoutException:
            print("❌ フォロワーポップアップが見つかりませんでした")
            return

        print("フォロワーリストのポップアップを検出")
        scrollable_element = self._find_scrollable_element(popup)
        if not scrollable_element:
            print("❌ スクロール可能な要素が見つかりませんでした")
            return

        initial_height = self.driver.execute_script(
            "return arguments[0].scrollHeight",
            scrollable_element,
        )
        print(f"初期スクロール高さ: {initial_height}px")

        for iteration in range(scroll_count):
            current_scroll = self.driver.execute_script(
                "return arguments[0].scrollTop",
                scrollable_element,
            )
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                scrollable_element,
            )
            new_position = current_scroll + SCROLL_STEP_PX
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[1]",
                scrollable_element,
                new_position,
            )

            time.sleep(scroll_pause)

            updated_scroll = self.driver.execute_script(
                "return arguments[0].scrollTop",
                scrollable_element,
            )
            updated_height = self.driver.execute_script(
                "return arguments[0].scrollHeight",
                scrollable_element,
            )

            print(f"📍 スクロール {iteration + 1}/{scroll_count}")
            print(
                f"   位置: {current_scroll}px → {updated_scroll}px, 高さ: {updated_height}px"
            )

            if updated_scroll == current_scroll and iteration > 0:
                print("⚠️ これ以上スクロールできません（最下部に到達）")
                break

        print("✅ スクロール完了")

    def _find_scrollable_element(self, popup: WebElement) -> Optional[WebElement]:
        try:
            all_divs = popup.find_elements(By.TAG_NAME, "div")
        except Exception as exc:
            print(f"スクロール要素探索中にエラー: {exc}")
            return None

        print(f"ポップアップ内のdiv要素数: {len(all_divs)}")
        for index, div in enumerate(all_divs):
            try:
                scroll_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight",
                    div,
                )
                client_height = self.driver.execute_script(
                    "return arguments[0].clientHeight",
                    div,
                )
            except Exception:
                continue

            if scroll_height > client_height > 100:
                print(f"✅ スクロール要素を発見（div #{index}）")
                print(
                    f"   scrollHeight: {scroll_height}px, clientHeight: {client_height}px"
                )
                return div
        return None

    def _find_follow_buttons(self, popup: WebElement) -> List[WebElement]:
        for by, locator in FOLLOW_BUTTON_QUERIES:
            try:
                buttons = popup.find_elements(by, locator)
            except Exception:
                buttons = []
            if buttons:
                print(f"   🔍 セレクター {locator} で {len(buttons)} 個のボタンを発見")
                return buttons

        try:
            all_buttons = popup.find_elements(By.TAG_NAME, "button")
        except Exception:
            return []

        result = [
            button
            for button in all_buttons
            if button.is_displayed() and button.text in {"フォロー", "Follow"}
        ]
        if result:
            print(f"   🔍 代替検索で {len(result)} 個のボタンを発見")
        return result

    def _handle_follow_dialog(self) -> bool:
        for xpath in (
            "//button[text()='OK' or text()='わかりました']",
            "//button[text()='閉じる' or text()='Close']",
        ):
            try:
                dialog_button = self.driver.find_element(By.XPATH, xpath)
                dialog_button.click()
                time.sleep(1.0)
                return True
            except NoSuchElementException:
                continue
        return False

    def _scroll_popup_slightly(self, popup: WebElement) -> None:
        scrollable_element = self._find_scrollable_element(popup)
        if not scrollable_element:
            return
        try:
            self.driver.execute_script(
                "arguments[0].scrollTop += arguments[1]",
                scrollable_element,
                SCROLL_STEP_PX,
            )
        except Exception as exc:
            print(f"   ⚠️  スクロール中にエラー: {exc}")

    def _get_username_from_button(self, button: WebElement) -> str:
        try:
            parent = button.find_element(By.XPATH, "./ancestor::div[contains(@class, 'x1dm5mii')]")
            username_element = parent.find_element(By.TAG_NAME, "span")
            return username_element.text
        except Exception:
            return "不明なユーザー"

    def _check_rate_limit(self, wait_seconds: float = 0) -> bool:
        deadline = time.time() + wait_seconds
        while True:
            try:
                dialogs = self.driver.find_elements(
                    By.XPATH,
                    "//div[@role='dialog' and (not(@aria-hidden) or @aria-hidden='false')]",
                )
                for dialog in dialogs:
                    if not dialog.is_displayed():
                        continue
                    text = dialog.text
                    if any(message in text for message in RATE_LIMIT_MESSAGES):
                        return True
            except Exception:
                pass
            if time.time() >= deadline:
                break
            time.sleep(0.25)
        return False

    @staticmethod
    def _create_driver() -> WebDriver:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--disable-features=PermissionsPolicy")

        service = Service(
            ChromeDriverManager().install(),
            log_path="NUL" if os.name == "nt" else "/dev/null",
        )
        return webdriver.Chrome(service=service, options=chrome_options)

    def _dismiss_save_login_popup(self) -> None:
        try:
            later_button = WebDriverWait(self.driver, MAX_POPUP_WAIT_SECONDS).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='後で']"))
            )
            later_button.click()
            time.sleep(1.0)
            print("「後で」ボタンをクリックしました")
        except TimeoutException:
            print("「後で」ボタンが見つかりませんでした")

    def _dismiss_notification_popup(self) -> None:
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
            time.sleep(1.0)
            print("通知ポップアップを閉じました")
        except TimeoutException:
            print("通知ポップアップは表示されませんでした")


def main() -> None:
    credentials = InstagramCredentials(username=USERNAME, password=PASSWORD)
    with InstaFollower(credentials) as bot:
        bot.login()
        bot.find_followers(TARGET_PROFILE_URL)
        bot.follow()


if __name__ == "__main__":
    main()
