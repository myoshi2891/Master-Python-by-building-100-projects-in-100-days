from __future__ import annotations

import os
import re
import time
import urllib.parse
from dataclasses import dataclass
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

GOOGLE_FORM_LINK = os.getenv("GOOGLE_FORM_LINK", "").strip()
FIELD_ORDER = [
    part.strip().lower()
    for part in os.getenv("GOOGLE_FORM_FIELD_ORDER", "address,price,link").split(",")
    if part.strip()
]
SHEET_BUTTON_LABELS = [
    part.strip()
    for part in os.getenv(
        "GOOGLE_FORM_SHEET_BUTTON_LABELS",
        "Create spreadsheet,スプレッドシートを作成,View responses in Sheets,スプレッドシートで表示",
    ).split(",")
    if part.strip()
]
SHEET_CONFIRM_TEXTS = [
    part.strip()
    for part in os.getenv(
        "GOOGLE_FORM_SHEET_CONFIRM_TEXTS",
        "Create,作成",
    ).split(",")
    if part.strip()
]

REPO_ROOT = Path(__file__).resolve().parent.parent
CHROME_PROFILE_DIR = REPO_ROOT / "chrome_profile"

BASE_URL = "https://appbrewery.github.io/Zillow-Clone/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
    "Referer": BASE_URL,
}

PRICE_RE = re.compile(r"\$\s*\d[\d,]*")
ADDR_NOISE_RE = re.compile(r"[\n\r]+|[|]")
WS_RE = re.compile(r"\s{2,}")


@dataclass
class Listing:
    address: str
    price: str
    link: str


def clean_price(raw: str) -> str | None:
    """'$2,895+/mo' -> '$2,895' のように整形。見つからなければ None。"""
    if not raw:
        return None
    match = PRICE_RE.search(raw)
    if not match:
        return None
    price = match.group(0).replace(" ", "")
    digits = re.sub(r"\D", "", price)
    if len(digits) < 3:
        return None
    return price


def clean_address(raw: str) -> str:
    """改行・パイプを除去し、余分な空白と末尾の区切りをトリム。"""
    if not raw:
        return ""
    sanitized = ADDR_NOISE_RE.sub(" ", raw)
    sanitized = WS_RE.sub(" ", sanitized)
    return sanitized.strip(" ,")


def fetch_html(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


def scrape_zillow_clone(url: str = BASE_URL) -> tuple[list[str], list[str], list[str]]:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    links: list[str] = []
    seen_links: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        text = anchor.get_text(strip=True)
        if "zillow.com" in href and text and ("," in text or "|" in text):
            full_href = href if href.startswith("http") else urllib.parse.urljoin(url, href)
            if full_href not in seen_links:
                seen_links.add(full_href)
                links.append(full_href)

    prices_raw: list[str] = []
    for node in soup.find_all(string=True):
        candidate = str(node).strip()
        if "$" in candidate:
            cleaned = clean_price(candidate)
            if cleaned:
                prices_raw.append(cleaned)
    prices = list(dict.fromkeys(prices_raw))

    addresses: list[str] = []
    for anchor in soup.find_all("a", href=True):
        if "zillow.com" in anchor["href"]:
            text = anchor.get_text(" ", strip=True)
            if ("," in text or "|" in text) and text:
                addresses.append(clean_address(text))
    addresses = list(dict.fromkeys(addresses))

    return links, prices, addresses


def compose_listings(links: list[str], prices: list[str], addresses: list[str]) -> list[Listing]:
    count = min(len(links), len(prices), len(addresses))
    if count == 0:
        return []
    if count < max(len(links), len(prices), len(addresses)):
        print(f"[WARN] Detected mismatched counts (links={len(links)}, prices={len(prices)}, addresses={len(addresses)}). Truncating to {count}.")
    listings = [
        Listing(address=addresses[idx], price=prices[idx], link=links[idx])
        for idx in range(count)
    ]
    return listings


def create_chrome_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    if CHROME_PROFILE_DIR.exists():
        options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
        default_profile = CHROME_PROFILE_DIR / "Default"
        if default_profile.exists():
            options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(0)
    return driver


def locate_question_inputs(driver: webdriver.Chrome, timeout: int = 20) -> list:
    wait = WebDriverWait(driver, timeout)
    list_items = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "form div[role='listitem']"))
    )
    fields: list = []
    for item in list_items:
        field = None
        for selector in ("input:not([type='hidden'])", "textarea"):
            candidates = item.find_elements(By.CSS_SELECTOR, selector)
            for candidate in candidates:
                if candidate.is_displayed():
                    field = candidate
                    break
            if field:
                break
        if field:
            fields.append(field)

    unique_fields: list = []
    seen_keys: set[str] = set()
    for element in fields:
        key = (
            element.get_attribute("id")
            or element.get_attribute("name")
            or element.get_attribute("aria-labelledby")
            or element.get_attribute("aria-describedby")
            or str(id(element))
        )
        if key in seen_keys:
            continue
        seen_keys.add(key)
        unique_fields.append(element)

    if unique_fields:
        return unique_fields

    fallback = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "form input:not([type='hidden']), form textarea")
        )
    )
    return [element for element in fallback if element.is_displayed()]


def fill_form_page(driver: webdriver.Chrome, listing: Listing, timeout: int = 20) -> None:
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form")))
    inputs = locate_question_inputs(driver, timeout=timeout)

    if len(inputs) < len(FIELD_ORDER):
        raise RuntimeError(
            f"Form offers only {len(inputs)} visible inputs but {len(FIELD_ORDER)} values are required."
        )

    for field_name, element in zip(FIELD_ORDER, inputs):
        value = getattr(listing, field_name, "")
        element.clear()
        element.send_keys(value)

    try:
        submit_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form div[role='button'][jsname='M2UYVd']"))
        )
    except TimeoutException:
        buttons = driver.find_elements(By.CSS_SELECTOR, "form div[role='button']")
        if not buttons:
            raise
        submit_button = buttons[-1]

    driver.execute_script("arguments[0].click();", submit_button)

    try:
        wait.until(EC.url_contains("formResponse"))
    except TimeoutException:
        try:
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'viewform')]"))
            )
        except TimeoutException:
            print("[WARN] Submission confirmation not detected; verify the form submission manually.")
    time.sleep(0.5)


def submit_listings_to_form(driver: webdriver.Chrome, form_url: str, listings: list[Listing]) -> str | None:
    if not listings:
        print("[INFO] No listings to submit to the form.")
        return None

    wait = WebDriverWait(driver, 20)
    driver.get(form_url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form")))
    resolved_form_url = driver.current_url

    total = len(listings)
    for idx, listing in enumerate(listings, start=1):
        if idx > 1:
            driver.get(resolved_form_url)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form")))
        fill_form_page(driver, listing)
        print(f"[INFO] Submitted {idx}/{total}: {listing.address} | {listing.price} | {listing.link}")

    return resolved_form_url


def derive_responses_url(form_url: str) -> str | None:
    if not form_url:
        return None
    parsed = urllib.parse.urlsplit(form_url)
    if "/viewform" not in parsed.path:
        return None
    responses_path = parsed.path.replace("/viewform", "/edit")
    clean = parsed._replace(path=responses_path, query="", fragment="")
    return urllib.parse.urlunsplit(clean) + "#responses"


def create_sheet_from_responses(driver: webdriver.Chrome, form_url: str) -> None:
    responses_url = derive_responses_url(form_url)
    if not responses_url:
        print("[WARN] Could not derive the responses URL from the provided form link. Skipping sheet creation.")
        return

    wait = WebDriverWait(driver, 30)
    driver.get(responses_url)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='tablist']")))
    except TimeoutException:
        print("[WARN] Unable to load the responses view. Make sure you have edit access to the form.")
        return

    handles_before = list(driver.window_handles)
    sheet_button = None

    for attr in ("aria-label", "data-tooltip"):
        for label in SHEET_BUTTON_LABELS:
            try:
                sheet_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//div[@role='button' and contains(@{attr}, '{label}')]")
                    )
                )
                break
            except TimeoutException:
                continue
        if sheet_button:
            break

    if not sheet_button:
        print("[WARN] Failed to locate the Sheets icon. It may already be linked or the label may differ.")
        return

    driver.execute_script("arguments[0].click();", sheet_button)

    try:
        WebDriverWait(driver, 5).until(lambda d: len(d.window_handles) > len(handles_before))
        print("[INFO] Opened the existing responses spreadsheet.")
        return
    except TimeoutException:
        pass

    try:
        dialog = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
        )
    except TimeoutException:
        print("[WARN] Spreadsheet creation dialog did not appear; please create the sheet manually.")
        return

    clicked = False
    for text in SHEET_CONFIRM_TEXTS:
        try:
            create_button = dialog.find_element(By.XPATH, f".//span[contains(text(), '{text}')]")
            driver.execute_script("arguments[0].click();", create_button)
            clicked = True
            break
        except NoSuchElementException:
            continue

    if not clicked:
        print("[WARN] Could not find the confirmation button in the spreadsheet dialog.")
        return

    try:
        WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > len(handles_before))
        print("[INFO] Created a new responses spreadsheet.")
    except TimeoutException:
        print("[WARN] Spreadsheet creation may have failed. Please verify in the browser.")


def main() -> None:
    links, prices, addresses = scrape_zillow_clone()
    listings = compose_listings(links, prices, addresses)

    if not listings:
        print("[INFO] No listings were scraped from the Zillow clone page.")
        return

    print(f"[INFO] Collected {len(listings)} listings from Zillow clone.")

    if not GOOGLE_FORM_LINK:
        print("[WARN] GOOGLE_FORM_LINK is not set. Aborting Selenium submission.")
        return

    driver = create_chrome_driver()
    try:
        resolved_form_url = submit_listings_to_form(driver, GOOGLE_FORM_LINK, listings)
        if resolved_form_url:
            create_sheet_from_responses(driver, resolved_form_url)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
