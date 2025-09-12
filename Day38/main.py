import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()


GENDER = os.getenv("GENDER")
weight_str = os.getenv("WEIGHT_KG")
if weight_str is None:
    raise ValueError("Environment variable WEIGHT_KG is not set")
WEIGHT_KG = float(weight_str)
height_str = os.getenv("HEIGHT_CM")
if height_str is None:
    raise ValueError("Environment variable HEIGHT_CM is not set")
HEIGHT_CM = float(height_str)
age_str = os.getenv("AGE")
if age_str is None:
    raise ValueError("Environment variable AGE is not set")
AGE = int(age_str)

APP_ID = os.getenv("APP_ID")  # YOUR APP ID
API_KEY = os.getenv("API_KEY")  # YOUR API KEY

USERNAME = os.getenv("USERNAME")
BASIC_TOKEN = os.getenv("BASIC_TOKEN")


exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

sheet_endpoint = os.getenv("SHEET_ENDPOINT")
if sheet_endpoint is None:
    raise ValueError("Environment variable SHEET_ENDPOINT is not set")

E_MAIL = os.getenv("E_MAIL")

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    # "Content-Type": "application/json",
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

if "exercises" not in result:
    print("API error:", result)
    exit()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

basic_token = os.getenv("BASIC_TOKEN", "").strip()
sheet_headers = {
    "Authorization": f"Basic {basic_token}",  # ← basic 必須
    "Content-Type": "application/json",
}

print("Using sheet auth header:", sheet_headers)

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        auth=(
            f'{USERNAME}',
            f'{BASIC_TOKEN}',
        ),
        headers=sheet_headers,
    )

    print(sheet_response.text)

    print("Endpoint:", sheet_endpoint)
    print("Headers:", sheet_headers)
    print("Payload:", json.dumps(sheet_inputs, indent=2))

    print("Status:", sheet_response.status_code)
    print("Response headers:", sheet_response.headers)
    print("repr token:", repr(basic_token))
