import smtplib

import requests
from bs4 import BeautifulSoup
from config import E_MAIL, E_MAIL2, PASSWORD, SMTP_ADDRESS,USER_AGENT

# url = "https://appbrewery.github.io/instant_pot/"
url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

# ====================== Add Headers to the Request ===========================

header = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "ja;q=0.2,en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.text, "html.parser")

price_element = soup.find(class_="a-offscreen")
if price_element is not None:
    price = price_element.get_text()

price_without_currency = price.split("$")[1]

price_as_float = float(price_without_currency)
# print(price_as_float)

# ====================== Send an Email ===========================

title_element = soup.find(id="productTitle")
if title_element is not None:
    title = title_element.get_text().strip()
# print(title)

BUY_PRICE = 100

if price_as_float < BUY_PRICE:
    message = f"{title} is now only ${price}!"

    with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        connection.login(user=E_MAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=E_MAIL,
            to_addrs=E_MAIL2,
            msg=f"Subject: Amazon Price Alert!\n\n{message}".encode("utf-8"),
        )
