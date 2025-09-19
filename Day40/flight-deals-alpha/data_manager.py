from pprint import pprint
from typing import Any, Dict, List

import requests
from config import (PRICES_ENDPOINT, SHEETY_PASSWORD, SHEETY_USER,
                    USERS_ENDPOINT)
from requests.auth import HTTPBasicAuth


class DataManager:
    """Manages interaction with the Google Sheet via Sheety API."""

    def __init__(self) -> None:
        """Initializes the DataManager."""
        self.users_endpoint = USERS_ENDPOINT
        self.prices_endpoint = PRICES_ENDPOINT
        self._auth = HTTPBasicAuth(str(SHEETY_USER), str(SHEETY_PASSWORD))

    def get_destination_data(self) -> List[Dict[str, Any]]:
        """Retrieves destination data from the Google Sheet."""
        try:
            response = requests.get(url=self.prices_endpoint, auth=self._auth)
            response.raise_for_status()
            data = response.json()
            return data.get("prices", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching destination data: {e}")
            return []

    def update_destination_codes(self, destination_data: List[Dict[str, Any]]) -> None:
        """Updates the IATA codes in the Google Sheet for each city."""
        if not destination_data:
            print("No destination data to update.")
            return

        for city in destination_data:
            if "iataCode" not in city or not city.get("iataCode"):
                continue

            new_data = {"price": {"iataCode": city["iataCode"]}}
            try:
                response = requests.put(
                    url=f"{self.prices_endpoint}/{city['id']}",
                    json=new_data,
                    auth=self._auth,
                )
                response.raise_for_status()
                # print(f"Successfully updated IATA code for {city['city']}.")
            except requests.exceptions.RequestException as e:
                print(f"Error updating IATA code for {city['city']}: {e}")

    def get_customer_emails(self) -> List[Dict[str, Any]]:
        """Retrieves customer email data from the Google Sheet."""
        try:
            response = requests.get(url=self.users_endpoint, auth=self._auth)
            response.raise_for_status()
            if response.text:
                data = response.json()
                return data.get("users", [])
            else:
                print("Customer data response is empty. No users found.")
                return []
        except requests.exceptions.JSONDecodeError:
            print("Error decoding JSON from customer emails response. The response may be empty.")
            if response.text:
                print("Response text:")
                pprint(response.text)
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching customer data: {e}")
            return []         
