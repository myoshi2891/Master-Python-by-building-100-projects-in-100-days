import os
from dotenv import load_dotenv
import requests
from twilio.rest import Client
load_dotenv()

account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_twilio = os.getenv("FROM_TWILIO")
twilio_sid = os.getenv("TWILIO_SID")
to_twilio = os.getenv("TO_TWILIO")

OWN_ENDPOINT: str = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = os.getenv("API_KEY")


weather_params = {
    "lat": 35.689487,
    "lon": 139.691711,
    "appid": API_KEY,
    "cnt": 4
}

will_rain = False
# def get_weather_data(city_name):
response = requests.get(OWN_ENDPOINT, params=weather_params)
if response.status_code == 200:
    weather_data = response.json()
    # weather_data["list"][0]["weather"][0]["id"]
    for hourly_data in weather_data["list"]:
        condition_code = hourly_data["weather"][0]["id"]
        print(condition_code)
        if int(condition_code) < 700:
            will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_= from_twilio,
    to=str(to_twilio),
    body="It's going to rain today. Remember to bring an ☔️"
    )
