"""
API client for exercise tracker application.
"""
import json

import requests

from config import APICredentials, UserProfile, SheetConfig
from models import ExerciseAPIResponse, WorkoutEntry


class NutritionixAPIClient:
    """Client for Nutritionix Exercise API."""

    BASE_URL = "https://trackapi.nutritionix.com/v2"

    def __init__(self, credentials: APICredentials) -> None:
        """Initialize API client with credentials."""
        self.credentials = credentials

    def get_exercises(self, query: str, user_profile: UserProfile) -> ExerciseAPIResponse:
        """Get exercise data from Nutritionix API."""
        endpoint = f"{self.BASE_URL}/natural/exercise"

        headers = {
            "x-app-id": self.credentials.app_id,
            "x-app-key": self.credentials.api_key,
        }

        parameters = {
            "query": query,
            "gender": user_profile.gender,
            "weight_kg": user_profile.weight_kg,
            "height_cm": user_profile.height_cm,
            "age": user_profile.age,
        }

        response = requests.post(endpoint, json=parameters, headers=headers)
        response.raise_for_status()

        return ExerciseAPIResponse.from_dict(response.json())


class SheetAPIClient:
    """Client for Sheet API."""

    def __init__(self, config: SheetConfig) -> None:
        """Initialize sheet API client with configuration."""
        self.config = config

    def add_workout(self, workout: WorkoutEntry) -> requests.Response:
        """Add workout entry to sheet."""
        basic_token = (self.config.basic_token or "").strip()

        headers = {
            "Authorization": f"Basic {basic_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.config.endpoint,
            json=workout.to_sheet_payload(),
            auth=(
                self.config.username or "",
                self.config.basic_token or "",
            ),
            headers=headers,
        )

        return response

    def log_request_details(
        self,
        workout: WorkoutEntry,
        response: requests.Response
    ) -> None:
        """Log request details for debugging."""
        basic_token = (self.config.basic_token or "").strip()

        headers = {
            "Authorization": f"Basic {basic_token}",
            "Content-Type": "application/json",
        }

        print("Response:", response.text)
        print("Endpoint:", self.config.endpoint)
        print("Headers:", headers)
        print("Payload:", json.dumps(workout.to_sheet_payload(), indent=2))
        print("Status:", response.status_code)
        print("Response headers:", dict(response.headers))
        print("repr token:", repr(basic_token))
