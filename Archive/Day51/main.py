import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Load environment variables from.env file
load_dotenv()

PROMISED_DOWN = 150
PROMISED_UP = 10
TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")


if not TWITTER_EMAIL or not TWITTER_PASSWORD:
    raise ValueError(
        "TWITTER_EMAIL and TWITTER_PASSWORD must be set in your environment."
    )


class InternetSpeedTwitterBot:
    def __init__(self, driver_path, email, password):
        self.driver = webdriver.Chrome()
        self.up = 0
        self.down = 0
        self.email = email
        self.password = password


    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")

        # accept_button = self.driver.find_element(By.ID, value="_evidon-banner-acceptbutton")
        # accept_button.click()

        time.sleep(3)

        go_button = self.driver.find_element(By.CSS_SELECTOR, value=".start-button a")
        go_button.click()

        time.sleep(60)

        self.up = self.driver.find_element(
            By.XPATH,
            value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span',
        ).text
        self.down = self.driver.find_element(
            By.XPATH,
            value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span',
        ).text

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/login")

        time.sleep(5)
        email = self.driver.find_element(
            By.XPATH,
            value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input',
        )
        password = self.driver.find_element(
            By.XPATH,
            value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input',
        )

        email.send_keys(self.email)
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)

        time.sleep(5)

        tweet_input = self.driver.find_element(
            By.CSS_SELECTOR, value="textarea.tweet-text"
        )
        tweet_input.send_keys(
            f"My internet speed is up: {self.up}, down: {self.down} Mbps. #InternetSpeedTest"
        )
        tweet_input.send_keys(Keys.ENTER)

        time.sleep(5)
        tweet_compose = self.driver.find_element(
            By.XPATH,
            value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div',
        )

        tweet = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
        tweet_compose.send_keys(tweet)
        time.sleep(3)

        tweet_button = self.driver.find_element(
            By.XPATH,
            value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]',
        )
        tweet_button.click()

        time.sleep(2)
        self.driver.quit()


bot = InternetSpeedTwitterBot(
    os.getenv(
        "CHROMEDRIVER_PATH"
        if os.getenv("CHROMEDRIVER_PATH")
        else "/path/to/chromedriver"
    ), TWITTER_EMAIL, TWITTER_PASSWORD
)
bot.get_internet_speed()
bot.tweet_at_provider()
