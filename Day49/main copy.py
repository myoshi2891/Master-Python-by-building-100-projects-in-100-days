from __future__ import annotations

import os
from dataclasses import dataclass
from time import sleep
from typing import Callable, TypeVar

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


TARGET_DAYS: tuple[str, ...] = ("Tue", "Thu")
TARGET_TIME: str = "6:00 PM"
RETRY_ATTEMPTS: int = 7
WAIT_TIMEOUT: int = 2


T = TypeVar("T")


load_dotenv()

ACCOUNT_EMAIL: str = os.getenv("ACCOUNT_EMAIL", "")
ACCOUNT_PASSWORD: str = os.getenv("ACCOUNT_PASSWORD", "")
GYM_URL: str = os.getenv("GYM_URL", "")


@dataclass
class BookingCounters:
    existing: int = 0
    booked: int = 0
    waitlisted: int = 0

    @property
    def total(self) -> int:
        return self.existing + self.booked + self.waitlisted


class GymBookingBot:
    def __init__(self, base_url: str, email: str, password: str) -> None:
        self.base_url = base_url
        self.email = email
        self.password = password
        self.driver: webdriver.Chrome = self._create_driver()
        self.wait: WebDriverWait = WebDriverWait(self.driver, WAIT_TIMEOUT)

    @staticmethod
    def _create_driver() -> webdriver.Chrome:
        service = Service(ChromeDriverManager().install(), log_path="chromedriver.log")

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

        return webdriver.Chrome(service=service, options=chrome_options)

    def run(self) -> None:
        print(self.base_url)
        self.driver.get(self.base_url)

        self.retry(self.login, description="login")
        counters, _ = self.process_class_cards()

        print(f"\n--- Total Tuesday/Thursday 6pm classes: {counters.total} ---")
        print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")

        verified = self.verify_bookings()

        print("\n--- VERIFICATION RESULT ---")
        print(f"Expected: {counters.total} bookings")
        print(f"Found: {verified} bookings")

        if counters.total == verified:
            print("✅ SUCCESS: All bookings verified!")
        else:
            print(f"❌ MISMATCH: Missing {counters.total - verified} bookings")

    def retry(
        self,
        func: Callable[[], T],
        *,
        retries: int = RETRY_ATTEMPTS,
        description: str = "operation",
    ) -> T:
        for attempt in range(1, retries + 1):
            try:
                return func()
            except TimeoutException:
                if attempt == retries:
                    raise
                print(f"Retrying {description} ({attempt}/{retries})")
                sleep(1)
        raise TimeoutException(f"{description} failed after {retries} attempts")

    def login(self) -> None:
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        )
        login_button.click()

        email_input = self.wait.until(EC.visibility_of_element_located((By.ID, "email-input")))
        email_input.clear()
        email_input.send_keys(self.email)

        password_input = self.driver.find_element(By.ID, "password-input")
        password_input.clear()
        password_input.send_keys(self.password)

        submit_button = self.driver.find_element(By.ID, "submit-button")
        submit_button.click()

        self.wait.until(EC.presence_of_element_located((By.ID, "schedule-page")))

    def process_class_cards(self) -> tuple[BookingCounters, list[str]]:
        counters = BookingCounters()
        processed_details: list[str] = []

        class_cards: list[WebElement] = self.driver.find_elements(
            By.CSS_SELECTOR, "div[id^='class-card-']"
        )
        for card in class_cards:
            try:
                day_title = self._get_day_title(card)
                if not self._is_target_day(day_title):
                    continue

                time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
                if not self._is_target_time(time_text):
                    continue

                class_name = card.find_element(By.CSS_SELECTOR, "h3").text
                button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")

                self._handle_booking(button, class_name, day_title, counters, processed_details)
            except NoSuchElementException:
                continue

        return counters, processed_details

    def _get_day_title(self, card: WebElement) -> str:
        day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
        return day_group.find_element(By.TAG_NAME, "h2").text

    @staticmethod
    def _is_target_day(day_title: str) -> bool:
        return any(target_day in day_title for target_day in TARGET_DAYS)

    @staticmethod
    def _is_target_time(time_text: str) -> bool:
        return TARGET_TIME in time_text

    def _handle_booking(
        self,
        button: WebElement,
        class_name: str,
        day_title: str,
        counters: BookingCounters,
        processed_details: list[str],
    ) -> None:
        state = button.text.strip()
        class_info = f"{class_name} on {day_title}"

        if state == "Booked":
            print(f"Already Booked: {class_info}")
            counters.existing += 1
            processed_details.append(f"[Booked] {class_info}")
        elif state == "Waitlisted":
            print(f"Already on Waitlisted: {class_info}")
            counters.existing += 1
            processed_details.append(f"[Waitlisted] {class_info}")
        elif state == "Book Class":
            self.retry(
                lambda: self._book(button, expected_text="Booked"),
                description=f"booking {class_info}",
            )
            counters.booked += 1
            print(f"You Booked: {class_info}")
            processed_details.append(f"[New Booking] {class_info}")
            sleep(0.5)
        elif state == "Join Waitlist":
            self.retry(
                lambda: self._book(button, expected_text="Waitlisted"),
                description=f"waitlisting {class_info}",
            )
            counters.waitlisted += 1
            print(f"You Joined Waitlist: {class_info}")
            processed_details.append(f"[New Waitlist] {class_info}")
            sleep(1)

    def _book(self, button: WebElement, *, expected_text: str) -> None:
        button_id = button.get_attribute("id")
        if button_id is None:
            raise ValueError("Booking button is missing an id attribute.")
        button.click()
        self.wait.until(
            EC.text_to_be_present_in_element((By.ID, button_id), expected_text)
        )

    def verify_bookings(self) -> int:
        cards: list[WebElement] = self.retry(
            self._load_my_bookings, description="get_my_bookings"
        )
        verified_count = 0

        for card in cards:
            try:
                when_paragraph = card.find_element(By.XPATH, ".//p[strong[text()='When:']]")
                when_text = when_paragraph.text

                if self._is_target_day(when_text) and self._is_target_time(when_text):
                    class_name = card.find_element(By.TAG_NAME, "h3").text
                    print(f"Verified: {class_name}")
                    verified_count += 1
            except NoSuchElementException:
                print("Unable to verify class in My Bookings page.")

        return verified_count

    def _load_my_bookings(self) -> list[WebElement]:
        my_bookings_link: WebElement = self.driver.find_element(By.ID, "my-bookings-link")
        my_bookings_link.click()

        self.wait.until(EC.presence_of_element_located((By.ID, "my-bookings-page")))

        cards: list[WebElement] = self.driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")
        if not cards:
            raise TimeoutException("No bookings found on My Bookings page.")
        return cards


def main() -> None:
    if not GYM_URL:
        raise RuntimeError("GYM_URL is not configured.")

    bot = GymBookingBot(GYM_URL, ACCOUNT_EMAIL, ACCOUNT_PASSWORD)
    bot.run()


if __name__ == "__main__":
    main()
