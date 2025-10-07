# Tested with the following package versions:
# beautifulsoup4==4.12.2
# requests==2.31.0
# selenium==4.15.1

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Final

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

load_dotenv()

GOOGLE_FORM_LINK: Final[str] = os.getenv("GOOGLE_FORM_LINK", "").strip()
ZILLOW_CLONE_URL: Final[str] = "https://appbrewery.github.io/Zillow-Clone/"

HEADERS: Final[dict[str, str]] = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/84.0.4147.125 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}

LINK_SELECTOR: Final[str] = ".StyledPropertyCardDataWrapper a"
ADDRESS_SELECTOR: Final[str] = ".StyledPropertyCardDataWrapper address"
PRICE_SELECTOR: Final[str] = ".PropertyCardWrapper span"

ADDRESS_XPATH: Final[str] = (
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
)
PRICE_XPATH: Final[str] = (
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
)
LINK_XPATH: Final[str] = (
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
)
SUBMIT_BUTTON_XPATH: Final[str] = (
    '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div'
)


@dataclass(frozen=True)
class Listing:
    address: str
    price: str
    link: str


def fetch_listings() -> list[Listing]:
    """Zillow クローンの HTML から Listing を抽出し、学習用途の print も残す。"""
    response: requests.Response = requests.get(ZILLOW_CLONE_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    all_link_elements = soup.select(LINK_SELECTOR)
    links: list[str] = [link["href"] for link in all_link_elements]
    print(f"There are {len(links)} links to individual listings in total: \n")
    print(links)

    all_address_elements = soup.select(ADDRESS_SELECTOR)
    addresses: list[str] = [
        address.get_text().replace(" | ", " ").strip() for address in all_address_elements
    ]
    print(f"\n After having been cleaned up, the {len(addresses)} addresses now look like this: \n")
    print(addresses)

    all_price_elements = soup.select(PRICE_SELECTOR)
    prices: list[str] = [
        price.get_text().replace("/mo", "").split("+")[0]
        for price in all_price_elements
        if "$" in price.text
    ]
    print(f"\n After having been cleaned up, the {len(prices)} prices now look like this: \n")
    print(prices)

    count = min(len(links), len(addresses), len(prices))
    if count == 0:
        return []

    listings = [
        Listing(address=addresses[idx], price=prices[idx], link=links[idx])
        for idx in range(count)
    ]
    return listings


def create_driver(detach: bool = True) -> tuple[ChromeWebDriver, bool]:
    """ChromeDriver を作成し、参照が切れてもブラウザを保持できるようにする。"""
    options = webdriver.ChromeOptions()
    if detach:
        options.add_experimental_option("detach", True)
    driver: ChromeWebDriver = webdriver.Chrome(options=options)
    return driver, detach


def fill_form(driver: ChromeWebDriver, listing: Listing) -> None:
    """Google フォームの既定 3 問に Listing の値を入力して送信する。"""
    driver.get(GOOGLE_FORM_LINK)
    time.sleep(2)

    address_input: WebElement = driver.find_element(By.XPATH, ADDRESS_XPATH)
    price_input: WebElement = driver.find_element(By.XPATH, PRICE_XPATH)
    link_input: WebElement = driver.find_element(By.XPATH, LINK_XPATH)
    submit_button: WebElement = driver.find_element(By.XPATH, SUBMIT_BUTTON_XPATH)

    address_input.send_keys(listing.address)
    price_input.send_keys(listing.price)
    link_input.send_keys(listing.link)
    submit_button.click()


def submit_listings(listings: list[Listing]) -> None:
    """全 Listing を順にフォームへ送信する。"""
    if not GOOGLE_FORM_LINK:
        raise ValueError("GOOGLE_FORM_LINK is not set. Update your .env file.")
    if not listings:
        print("No listings to submit.")
        return

    driver, detach = create_driver(detach=True)
    try:
        for index, listing in enumerate(listings, start=1):
            fill_form(driver, listing)
            print(f"Submitted {index}/{len(listings)}: {listing.address}")
    finally:
        # detach=False の場合のみ自動でブラウザを閉じる
        if not detach:
            driver.quit()


def main() -> None:
    listings = fetch_listings()
    submit_listings(listings)


if __name__ == "__main__":
    main()
