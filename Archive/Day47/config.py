import os
from dotenv import load_dotenv

# Load environment variables from.env file
load_dotenv()

# Retrieve environment variables
SMTP_ADDRESS = os.getenv("SMTP_ADDRESS", "")
USER_AGENT = os.getenv("USER_AGENT", "")
E_MAIL = os.getenv("E_MAIL", "")
E_MAIL2 = os.getenv("E_MAIL2", "")
PASSWORD = os.getenv("PASSWORD", "")
