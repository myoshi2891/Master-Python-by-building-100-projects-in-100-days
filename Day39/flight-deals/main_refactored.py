from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "LON"


def main() -> None:
    """Main function to run the flight deal finder."""
    data_manager = DataManager()
    flight_search = FlightSearch()
    notification_manager = NotificationManager()

    sheet_data = data_manager.get_destination_data()

    # Update IATA codes in Google Sheet if they are missing
    for row in sheet_data:
        if not row.get("iataCode"):
            row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

    tomorrow = datetime.now() + timedelta(days=1)
    six_months_from_today = datetime.now() + timedelta(days=180)

    # Search for flights for each destination
    for destination in sheet_data:
        iata_code = destination.get("iataCode")
        if not iata_code:
            continue

        print(f"Searching for flights to {destination['city']}...")
        flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            iata_code,
            from_time=tomorrow,
            to_time=six_months_from_today,
        )

        cheapest_flight = find_cheapest_flight(flights)
        if cheapest_flight is None:
            print(f"No flights found for {destination['city']}.")
            continue

        # Populate city names from sheet data
        cheapest_flight.origin_city = "London"  # Or fetch dynamically
        cheapest_flight.destination_city = destination["city"]

        # Send notification if the flight is cheaper than the price in the sheet
        if cheapest_flight.price < destination.get("lowestPrice", float('inf')):
            print(f"Found a cheap flight to {destination['city']}! Price: £{cheapest_flight.price}")
            notification_manager.send_sms(cheapest_flight)


if __name__ == "__main__":
    main()
