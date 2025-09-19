import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

from data_manager import DataManager
from flight_data import find_cheapest_flight
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "LON"

# with refactored data management classes you need to use this code below:

def update_iata_codes(data_manager: DataManager, flight_search: FlightSearch, sheet_data: List[Dict[str, Any]]) -> None:
    """Updates missing IATA codes in the Google Sheet."""
    print("Updating IATA codes...")
    updated = False
    for row in sheet_data:
        if not row.get("iataCode"):
            row["iataCode"] = flight_search.get_destination_code(row["city"])
            updated = True

    if updated:
        data_manager.update_destination_codes(sheet_data)
        print("IATA codes updated.")
    else:
        print("All IATA codes are already present.")


def check_and_notify_for_flights(
    destination: Dict[str, Any],
    flight_search: FlightSearch,
    notification_manager: NotificationManager,
    customer_email_list: List[str]
) -> None:
    """Searches for flights for a destination and sends notifications if a cheap flight is found."""
    iata_code = destination.get("iataCode")
    if not iata_code:
        return

    print(f"Searching for flights to {destination['city']}...")
    tomorrow = datetime.now() + timedelta(days=1)
    six_months_from_today = datetime.now() + timedelta(days=180)

    # Search for direct flights first
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA, iata_code, from_time=tomorrow, to_time=six_months_from_today, is_direct=True
    )
    cheapest_flight = find_cheapest_flight(flights)

    # If no direct flights, search for indirect flights
    if cheapest_flight is None:
        print(f"No direct flights to {destination['city']}. Looking for indirect flights...")
        indirect_flights = flight_search.check_flights(
            ORIGIN_CITY_IATA, iata_code, from_time=tomorrow, to_time=six_months_from_today, is_direct=False
        )
        cheapest_flight = find_cheapest_flight(indirect_flights)

    if cheapest_flight is None:
        print(f"No flights found for {destination['city']}.")
        return

    print(f"Cheapest flight price is: £{cheapest_flight.price}.")

    # Populate city names from sheet data
    cheapest_flight.origin_city = "London"
    cheapest_flight.destination_city = destination["city"]

    # Send notification if the flight is cheaper than the price in the sheet
    if cheapest_flight.price < destination.get("lowestPrice", float('inf')):
        if cheapest_flight.stops == 0:
            message = (f"Low price alert! Only GBP {cheapest_flight.price} to fly direct "
                       f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                       f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}.")
        else:
            message = (f"Low price alert! Only GBP {cheapest_flight.price} to fly "
                       f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                       f"with {cheapest_flight.stops} stop(s) "
                       f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}.")

        print(f"Check your email. Lower price flight found to {destination['city']}!")
        notification_manager.send_emails(email_list=customer_email_list, email_body=message)


def main() -> None:
    """Main function to run the flight deal finder."""
    data_manager = DataManager()
    flight_search = FlightSearch()
    notification_manager = NotificationManager()

    sheet_data = data_manager.get_destination_data()
    update_iata_codes(data_manager, flight_search, sheet_data)

    customer_data = data_manager.get_customer_emails()
    if not customer_data:
        print("No customer emails found.")
        return
    customer_email_list = [row["whatIsYourEmail"] for row in customer_data]
    print(f"Customer email list: {customer_email_list}")

    for destination in sheet_data:
        check_and_notify_for_flights(destination, flight_search, notification_manager, customer_email_list)
        time.sleep(2)  # To avoid hitting API rate limits


if __name__ == "__main__":
    main()
