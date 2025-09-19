import requests as request
from requests.auth import HTTPBasicAuth
from config import SHEETY_ENDPOINT, SHEETY_USER, SHEETY_PASSWORD


class DataManager:
    def __init__(self):
        self._endpoint = SHEETY_ENDPOINT
        self._user = SHEETY_USER
        self._password = SHEETY_PASSWORD
        self._authorization = HTTPBasicAuth(str(self._user), str(self._password))
        self.destination_data = {}

    def get_destination_data(self):
        response = request.get(url=self._endpoint, auth=self._authorization)
        data = response.json()
        self.destination_data = data["prices"]
        # pprint(self.destination_data)
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = request.put(
                url=f"{self._endpoint}/{city['id']}",
                json=new_data,
                auth=self._authorization
            )
            print(response.text)
