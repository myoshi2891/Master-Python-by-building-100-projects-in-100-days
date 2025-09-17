#!/usr/bin/env python3
"""
Main application for exercise tracker.
"""
import sys
from datetime import datetime
from typing import NoReturn

from api_client import NutritionixAPIClient, SheetAPIClient
from config import load_config
from models import WorkoutEntry


def get_user_input() -> str:
    """Get exercise input from user."""
    return input("Tell me which exercises you did: ")


def create_workout_entry(exercise_name: str, duration: float, calories: float) -> WorkoutEntry:
    """Create workout entry with current date and time."""
    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")

    return WorkoutEntry(
        date=today_date,
        time=now_time,
        exercise=exercise_name.title(),
        duration=duration,
        calories=calories
    )


def handle_error(message: str) -> NoReturn:
    """Handle error and exit application."""
    print(f"Error: {message}")
    sys.exit(1)


def main() -> None:
    """Main application function."""
    try:
        # Load configuration
        config = load_config()

        # Initialize API clients
        nutritionix_client = NutritionixAPIClient(config.api_credentials)
        sheet_client = SheetAPIClient(config.sheet_config)

        # Get user input
        exercise_text = get_user_input()

        # Get exercises from Nutritionix API
        try:
            api_response = nutritionix_client.get_exercises(exercise_text, config.user_profile)
        except Exception as e:
            handle_error(f"Failed to get exercise data: {e}")

        # Process each exercise
        for exercise in api_response.exercises:
            # Create workout entry
            workout = create_workout_entry(
                exercise.name,
                exercise.duration_min,
                exercise.nf_calories
            )

            # Add to sheet
            try:
                response = sheet_client.add_workout(workout)
                sheet_client.log_request_details(workout, response)
            except Exception as e:
                print(f"Failed to add workout to sheet: {e}")
                continue

    except ValueError as e:
        handle_error(str(e))
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        handle_error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
