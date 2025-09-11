import os
from typing import Optional, Any, Final
from dotenv import load_dotenv
import requests
from twilio.rest import Client

load_dotenv()

# 環境変数の取得
account_sid: Optional[str] = os.getenv("TWILIO_SID")
auth_token: Optional[str] = os.getenv("TWILIO_AUTH_TOKEN")
from_twilio: Optional[str] = os.getenv("FROM_TWILIO")
to_twilio: Optional[str] = os.getenv("TO_TWILIO")
api_key: Optional[str] = os.getenv("API_KEY")

OWN_ENDPOINT: Final[str] = "https://api.openweathermap.org/data/2.5/forecast"


def get_weather_data() -> Optional[dict[str, Any]]:
    """OpenWeather APIから天気データを取得する"""
    if not api_key:
        raise ValueError("API_KEY is not set in environment variables")

    weather_params: dict[str, Any] = {
        "lat": 35.689487,
        "lon": 139.691711,
        "appid": api_key,
        "cnt": 4,
    }

    response = requests.get(OWN_ENDPOINT, params=weather_params, timeout=10)
    if response.status_code == 200:
        return response.json()
    return None


def will_it_rain(weather_data: dict[str, Any]) -> bool:
    """天気データから雨が降るかどうかを判定"""
    for hourly_data in weather_data.get("list", []):
        condition_code: int = int(hourly_data["weather"][0]["id"])
        print(condition_code)  # デバッグ用
        if condition_code < 700:
            return True
    return False


def send_sms(body: str) -> None:
    """TwilioでSMSを送信"""
    if not account_sid or not auth_token or not from_twilio or not to_twilio:
        raise ValueError("Twilio environment variables are not set")

    client = Client(account_sid, auth_token)
    client.messages.create(
        from_=from_twilio,
        to=to_twilio,
        body=body,
    )


def main() -> None:
    weather_data = get_weather_data()
    if weather_data and will_it_rain(weather_data):
        send_sms("It's going to rain today. Remember to bring an ☔️")


if __name__ == "__main__":
    main()
