import requests
from requests.auth import HTTPBasicAuth
from typing import List, Dict, Any
from config import SHEETY_ENDPOINT, SHEETY_USER, SHEETY_PASSWORD


class DataManager:
    """Manages interaction with the Google Sheet via Sheety API."""

    def __init__(self) -> None:
        """Initializes the DataManager."""
        self._endpoint = SHEETY_ENDPOINT
        self._auth = HTTPBasicAuth(str(SHEETY_USER), str(SHEETY_PASSWORD))
        self.destination_data: List[Dict[str, Any]] = []
 
    def get_destination_data(self) -> List[Dict[str, Any]]:
        """Retrieves destination data from the Google Sheet."""
        try:
            response = requests.get(url=self._endpoint, auth=self._auth)
            response.raise_for_status()
            data = response.json()
            self.destination_data = data.get("prices", [])
            return self.destination_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching destination data: {e}")
            return []

    def update_destination_codes(self) -> None:
        """Updates the IATA codes in the Google Sheet for each city."""
        if not self.destination_data:
            print("No destination data to update.")
            return

        for city in self.destination_data:
            if "iataCode" not in city:
                continue

            new_data = {"price": {"iataCode": city["iataCode"]}}
            try:
                response = requests.put(
                    url=f"{self._endpoint}/{city['id']}",
                    json=new_data,
                    auth=self._auth,
                )
                response.raise_for_status()
                print(f"Successfully updated IATA code for {city['city']}.")
            except requests.exceptions.RequestException as e:
                print(f"Error updating IATA code for {city['city']}: {e}")
