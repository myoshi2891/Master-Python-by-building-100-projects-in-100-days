import logging
import os
from dataclasses import dataclass
from typing import Iterable, Tuple

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

SPEEDTEST_URL = "https://www.speedtest.net/"
TWITTER_LOGIN_URL = "https://twitter.com/login"


class SpeedTestLocators:
    GO_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, ".start-button a")
    DOWNLOAD_RESULT: Tuple[str, str] = (
        By.CSS_SELECTOR,
        "span.download-speed",
    )
    UPLOAD_RESULT: Tuple[str, str] = (
        By.CSS_SELECTOR,
        "span.upload-speed",
    )


class TwitterLocators:
    USERNAME_INPUT = [
        (By.NAME, "session[username_or_email]"),
        (By.NAME, "text"),
    ]
    PASSWORD_INPUT = [
        (By.NAME, "session[password]"),
        (By.NAME, "password"),
    ]
    TWEET_COMPOSE = [
        (By.CSS_SELECTOR, "div[data-testid='tweetTextarea_0']"),
        (By.CSS_SELECTOR, "div.public-DraftEditor-content"),
    ]
    TWEET_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "div[data-testid='tweetButtonInline']")


@dataclass
class BotConfig:
    promised_down: float
    promised_up: float
    tweet_template: str
    wait_timeout: int = 30


def get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"{name} must be set in your environment.")
    return value


def get_float_env(name: str, default: float) -> float:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    try:
        return float(raw_value)
    except ValueError as exc:  # pragma: no cover - defensive programming
        raise ValueError(f"{name} must be a numeric value.") from exc


def create_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    return webdriver.Chrome(options=options)


def wait_for_first_match(
    driver: WebDriver, locators: Iterable[Tuple[str, str]], timeout: int
) -> WebElement:
    for locator in locators:
        try:
            return WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            continue
    raise TimeoutException("None of the provided locators matched a visible element")


def wait_and_click(driver: WebDriver, locator: Tuple[str, str], timeout: int) -> None:
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator)).click()


def parse_speed(value: str) -> float:
    try:
        return float(value)
    except ValueError:  # pragma: no cover - defensive programming
        cleaned = value.replace("Mbps", "").strip()
        return float(cleaned)


class InternetSpeedTwitterBot:
    def __init__(self, driver: WebDriver, config: BotConfig, email: str, password: str):
        self.driver = driver
        self.config = config
        self.email = email
        self.password = password
        self.download_mbps = 0.0
        self.upload_mbps = 0.0

    def measure_speed(self) -> None:
        logger.info("Navigating to Speedtest")
        self.driver.get(SPEEDTEST_URL)
        wait_and_click(self.driver, SpeedTestLocators.GO_BUTTON, timeout=self.config.wait_timeout)

        logger.info("Waiting for speed test results")
        download_element = WebDriverWait(self.driver, 120).until(
            EC.visibility_of_element_located(SpeedTestLocators.DOWNLOAD_RESULT)
        )
        upload_element = WebDriverWait(self.driver, 120).until(
            EC.visibility_of_element_located(SpeedTestLocators.UPLOAD_RESULT)
        )
        self.download_mbps = parse_speed(download_element.text)
        self.upload_mbps = parse_speed(upload_element.text)
        logger.info("Measured speeds: %.2f down / %.2f up", self.download_mbps, self.upload_mbps)

    def login_to_twitter(self) -> None:
        logger.info("Logging into Twitter")
        self.driver.get(TWITTER_LOGIN_URL)

        username_field = wait_for_first_match(
            self.driver, TwitterLocators.USERNAME_INPUT, timeout=self.config.wait_timeout
        )
        username_field.send_keys(self.email)
        username_field.send_keys(Keys.ENTER)

        password_field = wait_for_first_match(
            self.driver, TwitterLocators.PASSWORD_INPUT, timeout=self.config.wait_timeout
        )
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.ENTER)

    def post_tweet(self, message: str) -> None:
        compose_area = wait_for_first_match(
            self.driver, TwitterLocators.TWEET_COMPOSE, timeout=self.config.wait_timeout
        )
        compose_area.click()
        compose_area.send_keys(message)
        wait_and_click(self.driver, TwitterLocators.TWEET_BUTTON, timeout=self.config.wait_timeout)
        logger.info("Tweet posted")

    def build_complaint_message(self) -> str:
        return self.config.tweet_template.format(
            down=self.download_mbps,
            up=self.upload_mbps,
            promised_down=self.config.promised_down,
            promised_up=self.config.promised_up,
        )

    def close(self) -> None:
        logger.info("Closing browser")
        self.driver.quit()


def main() -> None:
    email = get_required_env("TWITTER_EMAIL")
    password = get_required_env("TWITTER_PASSWORD")

    config = BotConfig(
        promised_down=get_float_env("PROMISED_DOWN", 150.0),
        promised_up=get_float_env("PROMISED_UP", 10.0),
        tweet_template=os.getenv(
            "TWEET_TEMPLATE",
            "Hey Internet Provider, my internet speed is {down:.2f}down/{up:.2f}up Mbps "
            "but I pay for {promised_down:.2f}down/{promised_up:.2f}up.",
        ),
        wait_timeout=int(get_float_env("SELENIUM_WAIT_TIMEOUT", 30.0)),
    )

    driver = create_driver()
    bot = InternetSpeedTwitterBot(driver=driver, config=config, email=email, password=password)

    try:
        bot.measure_speed()
        bot.login_to_twitter()
        bot.post_tweet(bot.build_complaint_message())
    finally:
        bot.close()


if __name__ == "__main__":
    main()

