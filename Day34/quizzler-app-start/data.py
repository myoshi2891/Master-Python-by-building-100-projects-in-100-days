from requests import get

params = {
    "amount": 10,
    "type": "boolean"
}

response = get("https://opentdb.com/api.php", params=params)
response.raise_for_status()
data = response.json()
question_data = data["results"]
