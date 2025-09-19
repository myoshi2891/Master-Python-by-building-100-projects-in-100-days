import requests
from datetime import datetime
from typing import Optional, List, Dict, Any

from config import (
    FLIGHT_ENDPOINT,
    TOKEN_ENDPOINT,
    FLIGHT_SEARCH_API_KEY,
    FLIGHT_SEARCH_API_SECRET,
    IATA_ENDPOINT
)


class FlightSearch:
    """Handles flight search operations using the Amadeus API."""

    def __init__(self) -> None:
        """Initializes the FlightSearch with API credentials and token."""
        self._api_key: str = FLIGHT_SEARCH_API_KEY
        self._api_secret: str = FLIGHT_SEARCH_API_SECRET
        self._token: Optional[str] = self._get_new_token()

    def _get_new_token(self) -> Optional[str]:
        """Fetches a new API token from the Amadeus token endpoint."""
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }
        try:
            response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
            response.raise_for_status()
            print("API token obtained successfully.")
            return response.json().get("access_token")
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining API token: {e}")
            return None

    def get_destination_code(self, city_name: str) -> str:
        """Retrieves the IATA code for a given city name."""
        if not self._token:
            print("Cannot get destination code without an API token.")
            return ""

        headers = {"Authorization": f"Bearer {self._token}"}
        query = {"keyword": city_name, "max": "2", "include": "AIRPORTS"}
        try:
            response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query)
            response.raise_for_status()
            data = response.json().get("data", [])
            return data[0].get("iataCode", "") if data else ""
        except requests.exceptions.RequestException as e:
            print(f"Error fetching IATA code for {city_name}: {e}")
            return ""
        except IndexError:
            print(f"No IATA code found for {city_name}.")
            return ""

    def check_flights(
        self,
        origin_city_code: str,
        destination_city_code: str,
        from_time: datetime,
        to_time: datetime,
        is_direct: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Searches for flights between two cities within a given date range.
        """
        if not self._token:
            print("Cannot check flights without an API token.")
            return []

        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true" if is_direct else "false",
            "currencyCode": "GBP",
            "max": 5,
        }
        try:
            response = requests.get(url=FLIGHT_ENDPOINT, headers=headers, params=query)
            response.raise_for_status()
            return response.json().get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"Error checking flights: {e}")
            return []

