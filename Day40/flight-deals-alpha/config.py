import os

from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
SHEETY_ENDPOINT = str(os.getenv("SHEETY_ENDPOINT"))
SHEETY_USER = str(os.getenv("SHEETY_USER"))
SHEETY_PASSWORD = str(os.getenv("SHEETY_PASSWORD"))

FROM_TWILIO: str = os.getenv("FROM_TWILIO", "")
TO_PHONE: str = os.getenv("TO_PHONE", "")

IATA_ENDPOINT: str = os.getenv("IATA_ENDPOINT", "")
FLIGHT_ENDPOINT: str = os.getenv("FLIGHT_ENDPOINT", "")
TOKEN_ENDPOINT: str = os.getenv("TOKEN_ENDPOINT", "")
FLIGHT_SEARCH_API_KEY: str = os.getenv("API_KEY", "")
FLIGHT_SEARCH_API_SECRET: str = os.getenv("API_SECRET", "")
# GET_FlIGHT_ENDPOINT: str = os.getenv("GET_FLIGHT_ENDPOINT", "")
PRICES_ENDPOINT: str = os.getenv("PRICES_ENDPOINT", "")
USERS_ENDPOINT: str = os.getenv("USERS_ENDPOINT", "")
EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
TEST_MAIL: str = os.getenv("TEST_MAIL", "")
TEST_MAIL2: str = os.getenv("TEST_MAIL2", "")
SMTP_SERVER: str = os.getenv("SMTP_SERVER", "")
SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
