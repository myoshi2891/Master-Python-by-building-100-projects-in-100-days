import os
from dotenv import load_dotenv

# Load environment variables from.env file
load_dotenv()

# Retrieve environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USERNAME = os.getenv("USERNAME")


