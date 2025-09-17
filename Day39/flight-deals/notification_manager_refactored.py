from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_TWILIO, TO_PHONE
from flight_data import FlightData


class NotificationManager:
    """Handles sending SMS notifications via Twilio."""

    def __init__(self) -> None:
        """Initializes the NotificationManager."""
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_TWILIO, TO_PHONE]):
            raise ValueError("Twilio configuration is missing in environment variables.")
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

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
