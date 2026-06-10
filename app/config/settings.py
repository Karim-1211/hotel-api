from pydantic_settings import BaseSettings
from urllib.parse import quote_plus


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    class Config:
        env_file = ".env"

    def get_db_url(self):
        password = quote_plus(self.DB_PASSWORD)

        return (
            f"postgresql://{self.DB_USER}:"
            f"{password}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )


# IMPORTANT: THIS LINE FIXES YOUR ERROR
settings = Settings()