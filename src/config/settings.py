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

    PRIVATE_JWT_KEY: str = "stub"
    PUBLIC_JWT_KEY: str = "stub"
    JWT_ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60000

    S3_ACCESS_TOKEN: str = "stub"
    S3_SECRET_KEY: str = "stub"
    S3_BUCKET_NAME: str = "stub"
    S3_DEFAULT_LINK: str = "stub"
    S3_ENDPOINT: str = "stub"

    DEBUG_SQL: bool = True
