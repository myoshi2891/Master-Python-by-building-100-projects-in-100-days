import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

token = os.getenv("TOKEN")
user_name = os.getenv("USERNAME")
GRAPH = "graph2"

pixela_url = "https://pixe.la/v1/users"

user_params = {
    "token": token,
    "username": user_name,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# response = requests.post(url=pixela_url, json=user_params)
# print(response.text)

graph_endpoint = f"{pixela_url}/{user_name}/graphs"

graph_config = {
    "id": GRAPH,
    "name": "Algorithm Graph",
    "unit": "hours",
    "type": "int",
    "color": "ajisai",
}

headers = {"X-USER-TOKEN": token}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.json())

pixel_creation_endpoint = f"{pixela_url}/{user_name}/graphs/{GRAPH}"

today = datetime(year=2025, month=5, day=6)

pixel_data = {
    "date": today.strftime("%Y%m%d"),
    "quantity": input("How many hours did you study today? "),
}

# response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)
# print(response.text)

update_endpoint = f"{pixela_url}/{user_name}/graphs/{GRAPH}/{today.strftime('%Y%m%d')}"

pixel_update_data = {
    "quantity": "15",
}

# response = requests.put(url=update_endpoint, json=pixel_update_data, headers=headers)
# print(response.text)

delete_endpoint = f"{pixela_url}/{user_name}/graphs/{GRAPH}/{today.strftime('%Y%m%d')}"
response = requests.delete(url=delete_endpoint, headers=headers)
print(response.text)
