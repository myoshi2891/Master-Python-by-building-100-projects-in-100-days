import smtplib
from typing import List

from config import (
    EMAIL_PASSWORD,
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
    """Handles sending SMS notifications via Twilio."""

    def __init__(self) -> None:
        """Initializes the NotificationManager."""
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_TWILIO, TO_PHONE]):
            raise ValueError(
                "Twilio configuration is missing in environment variables."
            )
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.email = TEST_MAIL
        self.email_password = EMAIL_PASSWORD
        self.connection = smtplib.SMTP(self.smtp_server, self.smtp_port)

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
            with smtplib.SMTP(SMTP_SERVER, port=SMTP_PORT) as connection:
                connection.starttls()
                connection.login(user=TEST_MAIL, password=EMAIL_PASSWORD)
                for email in email_list:
                    message = f"Subject:New Low Price Flight!\n\n{email_body}".encode(
                        "utf-8"
                    )
                    connection.sendmail(
                        from_addr=TEST_MAIL, to_addrs=email, msg=message
                    )
            print("Email sent successfully!")
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
