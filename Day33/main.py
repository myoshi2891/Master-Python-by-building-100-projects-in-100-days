import requests
from datetime import datetime
import time
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

TOKYO_LAT = 35.6895
TOKYO_LNG = 139.6917


email_address = os.getenv("TEST_MAIL1", "")
password = os.getenv("PASSWORD1", "")

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    #Youer position is within +5 or -5 degrees of the ISS position.
    if (TOKYO_LAT-5) <= iss_latitude <= (TOKYO_LAT+5) and (TOKYO_LNG-5) <= iss_longitude <= (TOKYO_LNG+5):
        print("Look up! The ISS is above you in the sky.")
        return True
    else:
        print("The ISS is not above you.")

def is_night():
    parameters = {
        "lat": TOKYO_LAT,
        "lng": TOKYO_LNG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json?", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=email_address, password=password)
            connection.sendmail(
                from_addr=email_address,
                to_addrs=email_address,
                msg="Subject:Look Up👆\n\nThe ISS is above you in the sky.",
            )


