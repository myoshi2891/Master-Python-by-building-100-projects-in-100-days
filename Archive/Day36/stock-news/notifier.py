from typing import Sequence
from twilio.rest import Client

from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_TWILIO, TO_PHONE


def send_sms(messages: Sequence[str]) -> None:
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and FROM_TWILIO and TO_PHONE):
        raise ValueError("Twilio configuration is missing in environment variables.")

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for msg in messages:
        message = client.messages.create(
            body=msg,
            from_=FROM_TWILIO,
            to=TO_PHONE,
        )
        print(f"SMS sent to {message.to}: {message.body}")
