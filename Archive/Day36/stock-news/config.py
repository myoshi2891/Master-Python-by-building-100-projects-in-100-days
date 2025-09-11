import os
from dotenv import load_dotenv

load_dotenv()

STOCK_API: str = os.getenv("STOCK_API", "")
NEWS_API: str = os.getenv("NEWS_API", "")
TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
FROM_TWILIO: str = os.getenv("FROM_TWILIO", "")
TO_PHONE: str = os.getenv("TO_PHONE", "")

STOCK_NAME: str = "TSLA"
COMPANY_NAME: str = "Tesla Inc"
STOCK_ENDPOINT: str = "https://www.alphavantage.co/query"
NEWS_ENDPOINT: str = "https://newsapi.org/v2/everything"
