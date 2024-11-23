import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from .settings import Settings

settings: Settings = Settings()
