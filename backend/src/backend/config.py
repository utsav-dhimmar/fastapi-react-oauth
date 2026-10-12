from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_CLIENT_SECRET: str = Field(...)
    GOOGLE_CLIENT_ID: str = Field(...)
    SECRET_KEY: str = Field(
        ..., description="kinldy generate using openssl rand -base64 32"
    )

    GOOGLE_AUTH_URL: str = Field(...)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Allows matching uppercase ENV keys to lowercase attributes
    )


settings = Settings()
