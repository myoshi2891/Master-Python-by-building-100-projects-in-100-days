import datetime

class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(
        self,
        origin_city,
        price,
        origin_airport,
        destination_city,
        destination_airport,
        # departureDate,
        out_date,
        return_date,
    ):
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        # self.departureDate = departureDate
        self.out_date = out_date
        self.return_date = return_date

def find_cheapest_flight(data):
    if data is None or not data['data']:
        print("No flights found.")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    first_flight = data['data'][0]
    lowest_price = float(first_flight['price']["grandTotal"])
    origin = first_flight['itineraries'][0]['segments'][0]['departure']['iataCode']
    destination = first_flight['itineraries'][0]['segments'][0]['arrival']['iataCode']
    out_date = first_flight['itineraries'][0]['segments'][0]['departure']['at'].split("T")[0]
    return_date = first_flight['itineraries'][1]['segments'][0]['departure']['at'].split("T")[0]

    cheapest_flight = FlightData(price=lowest_price, origin_city=origin, origin_airport=origin, destination_airport=destination, destination_city=destination, out_date=out_date, return_date=return_date, )

    for flight in data['data']:
        price = float(flight['price']["grandTotal"])
        if price < lowest_price:
            lowest_price = price
            origin = flight['itineraries'][0]['segments'][0]['departure']['iataCode']
            destination = flight['itineraries'][0]['segments'][0]['arrival']['iataCode']
            out_date = flight['itineraries'][0]['segments'][0]['departure']['at'].split("T")[0]
            return_date = flight['itineraries'][1]['segments'][0]['departure']['at'].split("T")[0]
            cheapest_flight = FlightData(price=lowest_price, origin_city=origin, origin_airport=origin, destination_city=destination, destination_airport=destination, out_date=out_date, return_date=return_date)

            print(f"Found cheapest flight: ${lowest_price} from {origin} to {destination} on {out_date}")
    return cheapest_flight
