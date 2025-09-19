from config import (
    FLIGHT_SEARCH_API_KEY,
    FLIGHT_SEARCH_API_SECRET,
    TOKEN_ENDPOINT,
    FLIGHT_ENDPOINT,
    IATA_ENDPOINT,
)
import requests


class FlightSearch:
    def __init__(self):
        """
        Initialize an instance of the FlightSearch class.
        This constructor performs the following tasks:
        1. Retrieves the API key and secret from the environment variables 'AMADEUS_API_KEY'
        and 'AMADEUS_SECRET' respectively.
        Instance Variables:
        _api_key (str): The API key for authenticating with Amadeus, sourced from the .env file
        _api_secret (str): The API secret for authenticating with Amadeus, sourced from the .env file.
        _token (str): The authentication token obtained by calling the _get_new_token() method.
        """

        self._api_key = FLIGHT_SEARCH_API_KEY
        self._api_secret = FLIGHT_SEARCH_API_SECRET
        self._token = self._get_new_token()  # Placeholder for the authentication token

    def _get_new_token(self):
        """
        Generates the authentication token used for accessing the Amadeus API and returns it.
        This function makes a POST request to the Amadeus token endpoint with the required
        credentials (API key and API secret) to obtain a new client credentials token.
        Upon receiving a response, the function updates the FlightSearch instance's token.
        Returns:
            str: The new access token obtained from the API response.
        """
        # Header with content type as per Amadeus documentation
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)

        # New bearer token. Typically expires in 1799 seconds (30min)
        # print(f"Your token is {response.json()['access_token']}")
        # print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()["access_token"]

    def get_destination_code(self, city_name):
        """
        Retrieves the IATA code for a specified city using the Amadeus Location API.
        Parameters:
        city_name (str): The name of the city for which to find the IATA code.
        Returns:
        str: The IATA code of the first matching city if found; "N/A" if no match is found due to an IndexError,
        or "Not Found" if no match is found due to a KeyError.

        The function sends a GET request to the IATA_ENDPOINT with a query that specifies the city
        name and other parameters to refine the search. It then attempts to extract the IATA code
        from the JSON response.
        - If the city is not found in the response data (i.e., the data array is empty, leading to
        an IndexError), it logs a message indicating that no airport code was found for the city and
        returns "N/A".
        - If the expected key is not found in the response (i.e., the 'iataCode' key is missing, leading
        to a KeyError), it logs a message indicating that no airport code was found for the city
        and returns "Not Found".
        """
        # print(f"Using this token inside get_destination_code: {self._token}")
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": 2,
            "include": "AIRPORTS",
        }
        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query)

        # print(
        #     f"Response status code: {response.status_code}. Airport IATA: {response.text}"
        # )
        try:
            code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"No airport code found for {city_name}.")
            return "Not Found"

        return code

    def check_flights(
        self, origin_city_code, destination_city_code, from_time, to_time
    ):
        """
        Retrieves flight details between two cities using the Amadeus Flight Search API.
        Parameters:
        origin_city_code (str): The IATA code of the origin city.
        destination_city_code (str): The IATA code of the destination city.
        from_time (str): The departure date and time in the format "YYYY-MM-DDThh:mm"
        to_time (str): The return date and time in the format "YYYY-MM-DDThh:mm"
        Returns:
        dict: A dictionary containing flight details if any flights are found; an empty dictionary
        if no flights are found due to an IndexError, or "Not Found" if no flights are found due to a KeyError.

        The function sends a GET request to the FLIGHT_ENDPOINT with a query that specifies the origin,
        destination, departure and return dates and times. It then attempts to extract the flight details
        from the JSON response.
        - If no flights are found in the response data (i.e., the data array is empty, leading to
        an IndexError), it logs a message indicating that no flights were found and returns an empty dictionary.
        - If the expected key is not found in the response (i.e., the 'flights' key is missing, leading
        to a KeyError), it logs a message indicating that no flights were found and returns an empty dictionary.
        """
        # print(f"Using this token inside check_flights: {self._token}")
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "max": 3,
            "currencyCode": "GBP",
        }

        response = requests.get(url=FLIGHT_ENDPOINT, headers=headers, params=query)
        print(
            f"Response status code: {response.status_code}. Flight search: {response.text}"
        )

        if response.status_code != 200:
            print(f"Error: Unable to fetch flight data. Status code: {response.status_code}")
            print(f"Response Body: {response.text}")
            return None
        try:
            data = response.json()
            return data
        except IndexError:
            print(f"No flights found for {origin_city_code} to {destination_city_code}.")
            return {}
        except KeyError:
            print(f"No flights found for {origin_city_code} to {destination_city_code}.")
            return "Not Found"
