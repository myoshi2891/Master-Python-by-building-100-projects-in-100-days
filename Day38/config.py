"""
Configuration module for exercise tracker application.
"""
import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass
class UserProfile:
    """User profile data class."""
    gender: Optional[str]
    weight_kg: float
    height_cm: float
    age: int


@dataclass
class APICredentials:
    """API credentials data class."""
    app_id: Optional[str]
    api_key: Optional[str]


@dataclass
class SheetConfig:
    """Sheet configuration data class."""
    endpoint: str
    username: Optional[str]
    basic_token: Optional[str]
    email: Optional[str]


@dataclass
class Config:
    """Main configuration class."""
    user_profile: UserProfile
    api_credentials: APICredentials
    sheet_config: SheetConfig


def load_config() -> Config:
    """Load configuration from environment variables."""
    load_dotenv()

    # Load user profile
    weight_str = os.getenv("WEIGHT_KG")
    if weight_str is None:
        raise ValueError("Environment variable WEIGHT_KG is not set")

    height_str = os.getenv("HEIGHT_CM")
    if height_str is None:
        raise ValueError("Environment variable HEIGHT_CM is not set")

    age_str = os.getenv("AGE")
    if age_str is None:
        raise ValueError("Environment variable AGE is not set")

    user_profile = UserProfile(
        gender=os.getenv("GENDER"),
        weight_kg=float(weight_str),
        height_cm=float(height_str),
        age=int(age_str)
    )

    # Load API credentials
    api_credentials = APICredentials(
        app_id=os.getenv("APP_ID"),
        api_key=os.getenv("API_KEY")
    )

    # Load sheet config
    sheet_endpoint = os.getenv("SHEET_ENDPOINT")
    if sheet_endpoint is None:
        raise ValueError("Environment variable SHEET_ENDPOINT is not set")

    sheet_config = SheetConfig(
        endpoint=sheet_endpoint,
        username=os.getenv("USERNAME"),
        basic_token=os.getenv("BASIC_TOKEN"),
        email=os.getenv("E_MAIL")
    )

    return Config(
        user_profile=user_profile,
        api_credentials=api_credentials,
        sheet_config=sheet_config
    )
