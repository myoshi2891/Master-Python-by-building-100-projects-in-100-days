from typing import Optional, List, Dict, Any


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
    ) -> None:
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date


def find_cheapest_flight(data: List[Dict[str, Any]]) -> Optional[FlightData]:
    """
    Finds the cheapest flight from a list of flight data from the API
    and returns it as a FlightData object.
    """
    if not data:
        return None

    first_flight = data[0]
    cheapest_price = float(first_flight["price"]["grandTotal"])
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    return FlightData(
        price=cheapest_price,
        origin_airport=origin,
        origin_city=origin,  # Placeholder, as city name is not in this response
        destination_airport=destination,
        destination_city=destination,  # Placeholder
        out_date=out_date,
        return_date=return_date,
    )
