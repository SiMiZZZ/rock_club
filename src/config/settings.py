from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_USER: str = "stub"
    DB_PASSWORD: str = "stub"
    DB_NAME: str = "stub"

    DEBUG_SQL: bool = True
