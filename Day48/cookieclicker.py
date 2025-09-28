from time import sleep, time

from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install(), log_path="chromedriver.log")


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://ozh.github.io/cookieclicker/")


def dismiss_cookie_banner():
    try:
        consent_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".cc_btn.cc_btn_accept_all"))
        )
        consent_button.click()
        return True
    except TimeoutException:
        return False


# Wait for the game to load
wait = WebDriverWait(driver, 180)
try:
    wait.until(lambda driver: driver.find_element(By.ID, value="langSelect-JA"))
    language_select = driver.find_element(By.ID, value="langSelect-JA")
    language_select.click()
except NoSuchElementException:
    print("Game did not load within 3 minutes.")

dismiss_cookie_banner()
# Wait for the game to load
# wait.until(lambda driver: driver.find_element(By.ID, value="bigCookie"))
# Click on the "Big Cookie" button
WebDriverWait(driver, 180)

item_ids = [f"product{i}" for i in range(18)]

wait_time = 10
timeout = time() + wait_time
five_min = time() + 30 * 1  # 5 minutes from now

big_cookie_button = driver.find_element(By.ID, value="bigCookie")

while True:
    sleep(0.01)
    big_cookie_button.click()
    if time() > timeout:
        try:
            cookies_element = driver.find_element(By.ID, value="cookies")
            cookies_text = cookies_element.text
            cookies_count_str = cookies_text.split()[0].replace(",", "")
            cookies_count = int(cookies_count_str.split("クッキー")[0])

            products = driver.find_elements(By.CSS_SELECTOR, value="div[id^='product']")
            best_item = None
            for product in reversed(products):
                product_class = product.get_attribute("class")
                if product_class and "enabled" in product_class:
                    best_item = product
                    break
            if best_item:
                try:
                    best_item.click()
                    product_id = best_item.get_attribute("id") or ""
                    if product_id:
                        product_name_id = product_id.replace("product", "productName")
                        product_name = driver.find_element(By.ID, value=product_name_id).text
                        print(f"Bought item: {product_name} ({product_id})")
                except ElementClickInterceptedException:
                    if dismiss_cookie_banner():
                        best_item.click()
                        product_id = best_item.get_attribute("id") or ""
                        if product_id:
                            product_name_id = product_id.replace("product", "productName")
                            product_name = driver.find_element(By.ID, value=product_name_id).text
                            print(
                                f"Bought item after dismissing banner: {product_name} ({product_id})"
                            )
        except NoSuchElementException:
            print("Game did not load within 3 minutes.")

        timeout = time() + wait_time

    if time() > five_min:
        try:
            cookies_element = driver.find_element(By.ID, value="cookies")
            print(f"You have {cookies_element.text} cookies")
            break
        except NoSuchElementException:
            print("Game Over")
            driver.quit()
            exit(1)
