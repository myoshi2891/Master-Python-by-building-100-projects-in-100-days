import os
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

load_dotenv()

FB_EMAIL = os.getenv("FB_EMAIL", "")
FB_PASSWORD = os.getenv("FB_PASSWORD", "")

if not FB_EMAIL or not FB_PASSWORD:
    raise ValueError("FB_EMAIL and FB_PASSWORD must be set in your environment.")

driver = webdriver.Chrome()

driver.get("http://www.tinder.com")

sleep(2)
login_button = driver.find_element(By.XPATH, value='//*[text()="Log in"]')
login_button.click()

sleep(2)
fb_login = driver.find_element(
    By.XPATH,
    value='//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button',
)
fb_login.click()

# Switch to Facebook login window
sleep(2)
base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)
print(driver.title)

# Login and hit enter
email = driver.find_element(By.XPATH, value='//*[@id="email"]')
password = driver.find_element(By.XPATH, value='//*[@id="pass"]')
email.send_keys(FB_EMAIL)
password.send_keys(FB_PASSWORD)
password.send_keys(Keys.ENTER)

# Switch back to Tinder window
driver.switch_to.window(base_window)
print(driver.title)

# Delay by 5 seconds to allow page to load.
sleep(5)

# Allow location
allow_location_button = driver.find_element(
    By.XPATH, value='//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'
)
allow_location_button.click()

# Disallow notifications
notifications_button = driver.find_element(
    By.XPATH, value='//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]'
)
notifications_button.click()

# Allow cookies
cookies = driver.find_element(
    By.XPATH, value='//*[@id="content"]/div/div[2]/div/div/div[1]/button'
)
cookies.click()

# Tinder free tier only allows 100 "Likes" per day. If you have a premium account, feel free to change to a while loop.
for n in range(100):
    # Add a 1 second delay between likes.
    sleep(1)

    try:
        print("called")
        like_button = driver.find_element(
            By.XPATH,
            value='//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button',
        )
        like_button.click()

    # Catches the cases where there is a "Matched" pop-up in front of the "Like" button:
    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element(By.CSS_SELECTOR, value=".itsAMatch a")
            match_popup.click()

        # Catches the cases where the "Like" button has not yet loaded, so wait 2 seconds before retrying.
        except NoSuchElementException:
            sleep(2)

driver.quit()
