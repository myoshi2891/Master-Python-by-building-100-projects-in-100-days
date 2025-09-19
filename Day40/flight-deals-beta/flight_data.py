from typing import Any, Dict, List, Optional


class FlightData:
    """Represents structured data for a single flight journey."""

    def __init__(
        self,
        price: float,
        origin_city: str,
        origin_airport: str,
        destination_city: str,
        destination_airport: str,
        out_date: str,
        return_date: str,
        stops: bool = False,
    ) -> None:
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops


def find_cheapest_flight(data: List[Dict[str, Any]]) -> Optional[FlightData]:
    """
    Finds the cheapest flight from a list of flight data from the API
    and returns it as a FlightData object.
    """
    if not data:
        return None

    cheapest_flight_data = data[0]
    lowest_price = float(cheapest_flight_data["price"]["grandTotal"])

    for flight_data in data[1:]:
        price = float(flight_data["price"]["grandTotal"])
        if price < lowest_price:
            lowest_price = price
            cheapest_flight_data = flight_data

    nr_stops = len(cheapest_flight_data["itineraries"][0]["segments"]) - 1
    origin = cheapest_flight_data["itineraries"][0]["segments"][0]["departure"][
        "iataCode"
    ]
    destination = cheapest_flight_data["itineraries"][0]["segments"][nr_stops][
        "arrival"
    ]["iataCode"]
    out_date = cheapest_flight_data["itineraries"][0]["segments"][0]["departure"][
        "at"
    ].split("T")[0]
    return_date = cheapest_flight_data["itineraries"][1]["segments"][0]["departure"][
        "at"
    ].split("T")[0]

    return FlightData(
        price=lowest_price,
        origin_city="",  # To be populated later
        origin_airport=origin,
        destination_city="",  # To be populated later
        destination_airport=destination,
        out_date=out_date,
        return_date=return_date,
        stops=nr_stops > 0,
    )
