# Solved Problem

You've encountered an interesting problem! The error `Error sending email: please run connect() first` happening after one successful email send is a classic sign that the SMTP connection is being closed and not re-opened for subsequent emails.

Your `main.py` loop calls `notification_manager.send_emails()` for each destination that has a cheap flight. The first call succeeds, but it likely closes the connection to the email server. When the loop continues and finds another cheap flight, the `send_emails` function is called again, but it tries to use a connection that is no longer active, leading to the error.

To fix this, you need to ensure that the `NotificationManager` can handle sending multiple emails across different calls. The best way to do this is to establish a new connection for each batch of emails you need to send.

I'll create a new `notification_manager.py` file for you in the `Day40/flight-deals-alpha` directory with the corrected logic. This implementation will use a `with` statement to manage the SMTP connection, which automatically handles connecting and disconnecting for each call to `send_emails`.

Here is the code for the new file:

```python
# notification_manager.py
import smtplib
from typing import List
from config import MY_EMAIL, MY_PASSWORD, SMTP_SERVER, SMTP_PORT


class NotificationManager:
    """Handles sending notifications via email."""

    def send_emails(self, email_list: List[str], email_body: str) -> None:
        """Sends an email to a list of recipients."""
        if not email_list:
            print("No customer emails to send.")
            return

        try:
            with smtplib.SMTP(SMTP_SERVER, port=SMTP_PORT) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                for email in email_list:
                    message = f"Subject:New Low Price Flight!\n\n{email_body}".encode("utf-8")
                    connection.sendmail(
                        from_addr=MY_EMAIL,
                        to_addrs=email,
                        msg=message
                    )
            print("Email sent successfully!")
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

```

## Why This Works

1. **Connection per Call**: The `with smtplib.SMTP(...)` block is inside the `send_emails` method. This means every time you call `send_emails` from your loop in `main.py`, it will:

   - Open a fresh connection to the SMTP server.
   - Log in.
   - Send all the emails for that specific flight deal.
   - Automatically close the connection when the `with` block is exited.

2. **Robustness**: This approach is more resilient. It doesn't rely on keeping a connection open for a long time, which can time out or cause other issues.

By replacing your existing `notification_manager.py` with this version, your program should now be able to send email notifications for every cheap flight it finds, not just the first one.

## main.py

1. **`update_iata_codes`**: A new function to handle the logic for checking and updating missing IATA codes in your Google Sheet.
2. **`check_and_notify_for_flights`**: This function will encapsulate the flight search, price comparison, and notification logic for a single destination.
3. **`main`**: The main function will now be much cleaner, responsible only for orchestrating the calls to the other functions.

## data_manager.py

The current implementation is a bit stateful, relying on data being fetched and stored in instance variables before other methods can use it. I'll refactor it to make the methods more self-contained and less dependent on the object's state. This will make the class more robust and easier to understand.

Here are the key changes:

1. **Stateless Methods**: I'll modify `update_destination_codes` to accept the destination data as an argument instead of relying on `self.destination_data`. This makes the method's behavior more explicit.
2. **Clearer Endpoint Naming**: I'll use the specific endpoint variables (`self.prices_endpoint` and `self.users_endpoint`) directly in the methods instead of the generic `self._endpoint`.
3. **Improved Initialization**: I'll remove the initialization of `destination_data` and `customer_data` as empty dictionaries in `__init__`, as they are no longer used to hold state across method calls.

Here is the refactored code for `data_manager.py`:

```python
data_manager.py
import requests
from requests.auth import HTTPBasicAuth
from typing import List, Dict, Any
from config import SHEETY_USER, SHEETY_PASSWORD, PRICES_ENDPOINT, USERS_ENDPOINT
from pprint import pprint


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
```

And to ensure the refactored `main.py` works correctly with these changes, here is a small adjustment to the `update_iata_codes` function within `main.py`:

```python
# main.py
# ... existing code
def update_iata_codes(data_manager: DataManager, flight_search: FlightSearch, sheet_data: List[Dict[str, Any]]) -> None:
    """Updates missing IATA codes in the Google Sheet."""
    print("Updating IATA codes...")
    updated = False
    for row in sheet_data:
        if not row.get("iataCode"):
            row["iataCode"] = flight_search.get_destination_code(row["city"])
            updated = True

    if updated:
        data_manager.update_destination_codes(sheet_data)
        print("IATA codes updated.")
    else:
        print("All IATA codes are already present.")


def check_and_notify_for_flights(
# ... existing code
```

This updated `DataManager` is now more modular and its methods are more predictable, which is a great improvement for maintainability

## flight_search.py

Here are the key improvements I'll make:

1. **Centralized API Request Handling**: I'll introduce a private helper method, `_make_request`, to handle the common logic for making authenticated API calls. This will encapsulate adding the authorization header and handling standard request exceptions, which are currently repeated in multiple methods.
2. **Simplified Method Logic**: The `get_destination_code` and `check_flights` methods will be simplified to use the new `_make_request` helper, making them cleaner and more focused on their specific tasks.
3. **Improved Readability**: By centralizing the request logic, the overall class becomes easier to read and maintain.

Here is the refactored code for `flight_search.py`:

```python
flight_search.py
import requests
from datetime import datetime
from typing import Optional, List, Dict, Any

from config import (
    FLIGHT_ENDPOINT,
    TOKEN_ENDPOINT,
    FLIGHT_SEARCH_API_KEY,
    FLIGHT_SEARCH_API_SECRET,
    IATA_ENDPOINT,
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

    def _make_request(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Makes an authenticated GET request to the Amadeus API."""
        if not self._token:
            print("Cannot make API request without a token.")
            return None

        headers = {"Authorization": f"Bearer {self._token}"}
        try:
            response = requests.get(url=url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None

    def get_destination_code(self, city_name: str) -> str:
        """Retrieves the IATA code for a given city name."""
        query = {"keyword": city_name, "max": "2", "include": "AIRPORTS"}
        response_data = self._make_request(url=IATA_ENDPOINT, params=query)

        if not response_data:
            print(f"Error fetching IATA code for {city_name}.")
            return ""

        try:
            data = response_data.get("data", [])
            return data[0].get("iataCode", "") if data else ""
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
        response_data = self._make_request(url=FLIGHT_ENDPOINT, params=query)

        if not response_data:
            print("Error checking flights.")
            return []

        return response_data.get("data", [])
```

## flight_data.py

1. **Correct the Loop**: The loop `for flight in data[:1]:` is a bug that only processes the first flight. I will change it to `for flight in data:` to correctly iterate through all available flights and find the actual cheapest one.
2. **Simplify Logic**: I will refactor the function to initialize the `cheapest_flight` with the first flight's data and then loop through the rest of the flights to find if a cheaper option exists. This makes the logic cleaner and removes redundant code.
3. **Calculate Stops Correctly**: The number of stops (`nr_stops`) will be calculated inside the loop for each flight to ensure it's accurate for the flight being processed.

Here is the refactored code for `flight_data.py`:

```python

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
    origin = cheapest_flight_data["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = cheapest_flight_data["itineraries"][0]["segments"][nr_stops]["arrival"]["iataCode"]
    out_date = cheapest_flight_data["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = cheapest_flight_data["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

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
```

## notification_manager.py

1. **Clean up Imports**: I'll add `FROM_EMAIL` to the imports from `config` for better readability when sending emails.
2. **Refine `__init__`**: I will remove the premature `smtplib.SMTP` connection, as it's better to establish the connection only when an email is being sent. I'll also add validation for email-related environment variables.
3. **Update `send_emails`**: I will use the new `FROM_EMAIL` variable as the sender's address.

Here is the refactored code for `notification_manager.py`:

```python
notification_manager.py
import smtplib
from typing import List

from config import (
    EMAIL_PASSWORD,
    FROM_EMAIL,
    FROM_TWILIO,
    SMTP_PORT,
    SMTP_SERVER,
    TEST_MAIL,
    TO_PHONE,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
)
from flight_data import FlightData
from twilio.rest import Client


class NotificationManager:
    """Handles sending SMS and email notifications."""

    def __init__(self) -> None:
        """Initializes the NotificationManager."""
        # Twilio configuration validation
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_TWILIO, TO_PHONE]):
            raise ValueError(
                "Twilio configuration is missing in environment variables."
            )
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Email configuration validation
        if not all([SMTP_SERVER, SMTP_PORT, FROM_EMAIL, EMAIL_PASSWORD]):
            raise ValueError(
                "Email configuration is missing in environment variables."
            )
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.from_email = FROM_EMAIL
        self.email_password = EMAIL_PASSWORD

    def send_sms(self, flight: FlightData) -> None:
        """Sends an SMS with the flight deal details."""
        message_body = (
            f"Low price alert! Only £{flight.price} to fly from "
            f"{flight.origin_city}-{flight.origin_airport} to "
            f"{flight.destination_city}-{flight.destination_airport}, "
            f"from {flight.out_date} to {flight.return_date}."
        )
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=FROM_TWILIO,
                to=TO_PHONE,
            )
            print(f"SMS sent successfully! SID: {message.sid}")
        except Exception as e:
            print(f"Error sending SMS: {e}")

    def send_emails(self, email_list: List[str], email_body: str) -> None:
        """Sends an email to a list of recipients."""
        if not email_list:
            print("No customer emails to send.")
            return

        try:
            with smtplib.SMTP(self.smtp_server, port=self.smtp_port) as connection:
                connection.starttls()
                connection.login(user=self.from_email, password=self.email_password)
                for email in email_list:
                    message = f"Subject:New Low Price Flight!\n\n{email_body}".encode(
                        "utf-8"
                    )
                    connection.sendmail(
                        from_addr=self.from_email, to_addrs=email, msg=message
                    )
            print("Emails sent successfully!")
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
```
