from os import path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "SynerevalAI"
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    OPENAI_API_KEY: str
    PROD: bool = False

    class Config:
        case_sensitive = True
        extra = "ignore"
        env_file = path.join(path.dirname(__file__), "..", "..", ".env")


settings = Settings()