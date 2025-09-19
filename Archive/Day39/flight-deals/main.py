from data_manager import DataManager
from flight_search import FlightSearch
import time
from datetime import datetime, timedelta
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager
#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
# print(sheet_data)
flight_search = FlightSearch()

origin_city_code = "LON"

# ==================== Update the Airport Codes in Google Sheet ====================

#  In main.py check if sheet_data contains any values for the "iataCode" key.
#  If not, then the IATA Codes column is empty in the Google Sheet.
#  In this case, pass each city name in sheet_data one-by-one
#  to the FlightSearch class to get the corresponding IATA code
#  for that city using the API.
#  You should use the code you get back to update the sheet_data dictionary.

for row in sheet_data:
    if sheet_data[0]["iataCode"] == "":
        from flight_search import FlightSearch
        flight_search = FlightSearch()
        for row in sheet_data:
            city_code = flight_search.get_destination_code(row["city"])
            row["iataCode"] = city_code
            time.sleep(2)  # To avoid hitting the API rate limit
        # print(f"sheet_data: {sheet_data}")

        data_manager.destination_data = sheet_data
        data_manager.get_destination_data()

tomorrow_date = datetime.now() + timedelta(days=1)
six_months_later = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        origin_city_code,
        destination["iataCode"],
        from_time=tomorrow_date,
        to_time=six_months_later,
    )
    if flight is None:
        print(f"No flights found for {destination['city']}.")
        continue

    cheapest_flight = find_cheapest_flight(flight)

    if cheapest_flight.price == "N/A":
        continue

      # --- START DEBUGGING BLOCK ---
    print("\n--- Checking for low price ---")
    print(f"Found flight price: £{cheapest_flight.price}")
    print(f"Your target price: £{destination['lowestPrice']}")
    # --- END DEBUGGING BLOCK ---
    if int(cheapest_flight.price) < int(destination["lowestPrice"]):
        print(
            f"Low price alert! Only £{cheapest_flight.price} to fly from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, from {cheapest_flight.out_date} to {cheapest_flight.return_date}."
        )

    if int(cheapest_flight.price) < int(destination["lowestPrice"]):
        print(
            f"Low price alert! Only £{cheapest_flight.price} to fly from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, from {cheapest_flight.out_date} to {cheapest_flight.return_date}."
        )

    if cheapest_flight.price != "N/A" and int(cheapest_flight.price) < int(destination["lowestPrice"]):
        print("Condition met! Preparing to send notification...")

        notification_manager = NotificationManager()
        message = f"Low price alert! Only £{cheapest_flight.price} to fly from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, from {cheapest_flight.out_date} to {cheapest_flight.return_date}."
        notification_manager.send_sms(message)

        # print(notification_manager.send_whatsapp)
        # message = f"Low price alert! Only £{cheapest_flight.price} to fly from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, from {cheapest_flight.out_date} to {cheapest_flight.return_date}."
        # notification_manager.send_whatsapp(message)
