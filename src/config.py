from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AgVefr Backend"
    admin_email: str
    DATABASE_URL: str
    secret_key: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
