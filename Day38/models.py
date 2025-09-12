"""
Data models for exercise tracker application.
"""
from dataclasses import dataclass
from typing import List, Any, Dict


@dataclass
class Exercise:
    """Exercise data model."""
    name: str
    duration_min: float
    nf_calories: float

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'Exercise':
        """Create Exercise instance from API response data."""
        return cls(
            name=data["name"],
            duration_min=data["duration_min"],
            nf_calories=data["nf_calories"]
        )


@dataclass
class ExerciseAPIResponse:
    """Response from Nutritionix exercise API."""
    exercises: List[Exercise]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExerciseAPIResponse':
        """Create ExerciseAPIResponse from dictionary."""
        if "exercises" not in data:
            raise ValueError(f"API error: {data}")

        exercises = [Exercise.from_api_response(ex) for ex in data["exercises"]]
        return cls(exercises=exercises)


@dataclass
class WorkoutEntry:
    """Workout entry for sheet."""
    date: str
    time: str
    exercise: str
    duration: float
    calories: float

    def to_sheet_payload(self) -> Dict[str, Dict[str, Any]]:
        """Convert to sheet API payload format."""
        return {
            "workout": {
                "date": self.date,
                "time": self.time,
                "exercise": self.exercise,
                "duration": self.duration,
                "calories": self.calories,
            }
        }
