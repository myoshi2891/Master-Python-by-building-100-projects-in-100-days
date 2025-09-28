import smtplib
import sys
from typing import Dict, Optional, Tuple

import requests
from bs4 import BeautifulSoup, Tag
from config import E_MAIL, E_MAIL2, PASSWORD, SMTP_ADDRESS, USER_AGENT

# ====================== Constants ===========================

PRODUCT_URL: str = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
BUY_PRICE: float = 100.0
REQUEST_HEADERS: Dict[str, str] = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",  # To get consistent price format ($)
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
}


def fetch_product_data(
    url: str, headers: Dict[str, str]
) -> Optional[Tuple[float, str]]:
    """Fetches product price and title from the given URL."""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    price_element: Optional[Tag] = soup.find(class_="a-offscreen")
    title_element: Optional[Tag] = soup.find(id="productTitle")

    if not price_element or not title_element:
        print(
            "Could not find price or title element. The page layout may have changed."
        )
        return None

    price_str: str = price_element.get_text()
    title: str = title_element.get_text().strip()

    try:
        # Remove currency symbols like '$' and convert to float
        price_without_currency = "".join(
            filter(lambda char: char.isdigit() or char == ".", price_str)
        )
        price_as_float = float(price_without_currency)
        return price_as_float, title
    except (ValueError, IndexError) as e:
        print(f"Could not parse the price: {price_str}. Error: {e}")
        return None


def send_email_alert(product_title: str, current_price: float) -> None:
    """Sends an email alert if the price is below the target."""
    message = f"{product_title} is now only ${current_price}!\n\nCheck it out here:\n{PRODUCT_URL}"
    email_content = f"Subject:Amazon Price Alert!\n\n{message}".encode("utf-8")

    try:
        with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
            connection.starttls()
            connection.login(user=E_MAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=E_MAIL,
                to_addrs=E_MAIL2,
                msg=email_content,
            )
        print("Email alert sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")


def main() -> None:
    """Main function to check product price and send an alert."""
    if not all([E_MAIL, E_MAIL2, PASSWORD, SMTP_ADDRESS, USER_AGENT]):
        print("One or more environment variables are not set. Exiting.")
        sys.exit(1)

    product_data = fetch_product_data(PRODUCT_URL, REQUEST_HEADERS)

    if product_data is None:
        print("Failed to retrieve product data. Exiting.")
        sys.exit(1)

    price_as_float, title = product_data
    print(f"Retrieved product: {title}")
    print(f"Current price: ${price_as_float}")

    if price_as_float < BUY_PRICE:
        print(f"Price is below ${BUY_PRICE}. Sending an email alert...")
        send_email_alert(product_title=title, current_price=price_as_float)
    else:
        print(f"Price is not below the target of ${BUY_PRICE}.")


if __name__ == "__main__":
    main()
