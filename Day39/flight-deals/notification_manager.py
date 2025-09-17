from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_TWILIO, TO_PHONE

class NotificationManager:

    def __init__(self):
        if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and FROM_TWILIO and TO_PHONE):
            raise ValueError("Twilio configuration is missing in environment variables.")

           # --- START DEBUGGING BLOCK ---
        print("\n--- Initializing NotificationManager ---")
        # Print only the last 4 characters to avoid exposing full credentials
        print(f"FROM_TWILIO: {FROM_TWILIO}")
        print(f"TO_PHONE: {TO_PHONE}")
        print("--------------------------------------\n")
        # --- END DEBUGGING BLOCK ---

        self.account_sid = TWILIO_ACCOUNT_SID
        self.auth_token = TWILIO_AUTH_TOKEN
        self.from_phone = FROM_TWILIO
        self.to_phone = TO_PHONE
        self.client = Client(self.account_sid, self.auth_token)
        print(f"Twilio client initialized. From: {self.from_phone}, To: {self.to_phone}")

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=self.from_phone,
            to=self.to_phone
        )
        print(f"Message sent with SID: {message.sid}")
    # def send_whatsapp(self, message):
    #     message = self.client.messages.create(
    #         body=message,
    #         from_=f"whatsapp: {self.from_phone}",
    #         to=f"whatsapp: {self.to_phone}"
    #     )
    #     print(f"Message sent with SID: {message.sid}")
