from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager
import time

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

    # ==================== Retrieve your customer emails ====================

    customer_data = data_manager.get_customer_emails()
    if not customer_data:
        print("No customer emails found.")
        return
    customer_email_list = [row["whatIsYourEmail"] for row in customer_data]
    print(f"Customer email list: {customer_email_list}")

    # ==================== Search for direct flights  ====================
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
        time.sleep(2)  # To avoid hitting API rate limits
        if cheapest_flight is None:
            print(f"No flights found for {destination['city']}.")
            continue

        if cheapest_flight.price is None:
            print(f"No direct flights to {destination['city']}. Looking for indirect flights...")
            indirect_flights = flight_search.check_flights(
                ORIGIN_CITY_IATA,
                iata_code,
                from_time=tomorrow,
                to_time=six_months_from_today,
                is_direct=False
                )
            cheapest_flight = find_cheapest_flight(indirect_flights)
            if cheapest_flight is None:
                print(f"No indirect flights found for {destination['city']}.")
                continue
            print(f"Cheapest indirect flight price is: {(cheapest_flight.price)}.")


        # Populate city names from sheet data
        cheapest_flight.origin_city = "London"  # Or fetch dynamically
        cheapest_flight.destination_city = destination["city"]

        # Send notification if the flight is cheaper than the price in the sheet
        if cheapest_flight.price < destination.get("lowestPrice", float('inf')):
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly direct "\
            f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
            f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly "\
            f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
            f"with {cheapest_flight.stops} stop(s) "\
            f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        print(f"Check your email. Lower price flight found to {destination['city']}!")

        notification_manager.send_emails(email_list=customer_email_list, email_body=message)

        # notification_manager.send_sms(cheapest_flight)

if __name__ == "__main__":
    main()
