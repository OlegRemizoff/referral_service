from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_PASS: str
    DB_USER: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str

    EMAIL_SENDER: str
    EMAIL_PASSWORD: str
    class Config:
        env_file = ".env"

settings = Settings()


DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"