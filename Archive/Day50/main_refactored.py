import logging
import os
from time import sleep
from typing import Tuple

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TINDER_URL = "https://www.tinder.com"


class Locators:
    """Central definition of Selenium locators used in this script."""

    LOGIN_BUTTON: Tuple[str, str] = (By.XPATH, '//*[text()="Log in"]')
    FB_LOGIN_BUTTON: Tuple[str, str] = (
        By.XPATH,
        '//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button',
    )
    FB_EMAIL_INPUT: Tuple[str, str] = (By.ID, "email")
    FB_PASSWORD_INPUT: Tuple[str, str] = (By.ID, "pass")
    ALLOW_LOCATION_BUTTON: Tuple[str, str] = (
        By.XPATH,
        '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]',
    )
    DISABLE_NOTIFICATIONS_BUTTON: Tuple[str, str] = (
        By.XPATH,
        '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]',
    )
    ACCEPT_COOKIES_BUTTON: Tuple[str, str] = (
        By.XPATH,
        '//*[@id="content"]/div/div[2]/div/div/div[1]/button',
    )
    LIKE_BUTTON: Tuple[str, str] = (
        By.XPATH,
        '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button',
    )
    MATCH_POPUP_LINK: Tuple[str, str] = (By.CSS_SELECTOR, ".itsAMatch a")


def get_required_env(name: str) -> str:
    """Return required environment variable or raise a helpful error."""

    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"{name} must be set in your environment.")
    return value


def get_int_env(name: str, default: int) -> int:
    """Return an integer environment variable with validation."""

    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    try:
        return int(raw_value)
    except ValueError as exc:  # pragma: no cover - defensive programming
        raise ValueError(f"{name} must be an integer value.") from exc


def get_float_env(name: str, default: float) -> float:
    """Return a float environment variable with validation."""

    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    try:
        return float(raw_value)
    except ValueError as exc:  # pragma: no cover - defensive programming
        raise ValueError(f"{name} must be a numeric value.") from exc


def build_driver() -> WebDriver:
    """Create a Chrome WebDriver with sensible defaults."""

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)


def wait_for_window_count(driver: WebDriver, expected_count: int, timeout: int = 10) -> None:
    """Block until the desired number of browser windows is available."""

    WebDriverWait(driver, timeout).until(lambda d: len(d.window_handles) >= expected_count)


def click_when_clickable(driver: WebDriver, locator: Tuple[str, str], timeout: int = 15) -> None:
    """Wait for an element to be clickable and click it."""

    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator)).click()


def find_visible_element(
    driver: WebDriver, locator: Tuple[str, str], timeout: int = 15
):
    """Wait for an element to be visible and return it."""

    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def click_if_present(driver: WebDriver, locator: Tuple[str, str], timeout: int = 5) -> bool:
    """Attempt to click an element if it becomes available within the timeout."""

    try:
        click_when_clickable(driver, locator, timeout=timeout)
        return True
    except TimeoutException:
        return False


def login_with_facebook(driver: WebDriver, email: str, password: str) -> None:
    """Handle the Tinder login flow using Facebook credentials."""

    base_window = driver.current_window_handle
    click_when_clickable(driver, Locators.LOGIN_BUTTON)
    click_when_clickable(driver, Locators.FB_LOGIN_BUTTON)

    wait_for_window_count(driver, expected_count=2)
    fb_window = next(handle for handle in driver.window_handles if handle != base_window)
    driver.switch_to.window(fb_window)

    logger.info("Logging into Facebook window: %s", driver.title)
    email_field = find_visible_element(driver, Locators.FB_EMAIL_INPUT)
    password_field = find_visible_element(driver, Locators.FB_PASSWORD_INPUT)
    email_field.send_keys(email)
    password_field.send_keys(password)
    password_field.send_keys(Keys.ENTER)

    # Wait for Tinder window to become active again.
    WebDriverWait(driver, 20).until(lambda d: base_window in d.window_handles)
    driver.switch_to.window(base_window)
    logger.info("Returned to Tinder window: %s", driver.title)


def dismiss_initial_modals(driver: WebDriver) -> None:
    """Handle location, notification, and cookie dialogs when they appear."""

    click_if_present(driver, Locators.ALLOW_LOCATION_BUTTON)
    click_if_present(driver, Locators.DISABLE_NOTIFICATIONS_BUTTON)
    click_if_present(driver, Locators.ACCEPT_COOKIES_BUTTON)


def handle_match_popup(driver: WebDriver) -> bool:
    """Close the match popup if it is currently blocking interactions."""

    try:
        click_when_clickable(driver, Locators.MATCH_POPUP_LINK, timeout=3)
        logger.info("Closed match popup.")
        return True
    except TimeoutException:
        return False
    except NoSuchElementException:
        return False


def like_profiles(driver: WebDriver, like_limit: int, delay_seconds: float) -> None:
    """Repeatedly click the Like button up to the configured limit."""

    for count in range(1, like_limit + 1):
        if delay_seconds > 0:
            sleep(delay_seconds)

        try:
            click_when_clickable(driver, Locators.LIKE_BUTTON)
            logger.info("Liked profile %s/%s", count, like_limit)
        except ElementClickInterceptedException:
            if handle_match_popup(driver):
                continue
            logger.warning("Like button intercepted; waiting briefly before retrying.")
            sleep(2)
        except TimeoutException:
            logger.warning("Like button not ready; retrying after short wait.")
            sleep(2)


def main() -> None:
    email = get_required_env("FB_EMAIL")
    password = get_required_env("FB_PASSWORD")
    like_limit = get_int_env("LIKE_LIMIT", default=100)
    delay_seconds = get_float_env("LIKE_DELAY_SECONDS", default=1.0)

    driver = build_driver()
    try:
        driver.get(TINDER_URL)
        login_with_facebook(driver, email, password)
        dismiss_initial_modals(driver)
        like_profiles(driver, like_limit=like_limit, delay_seconds=delay_seconds)
    finally:
        driver.quit()
        logger.info("Browser closed.")


if __name__ == "__main__":
    main()
