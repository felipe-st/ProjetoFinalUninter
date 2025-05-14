from typing import List

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:100%Vasco@localhost:5432/uninter'
    DBBaseModel = declarative_base()
    JWT_SECRET: str = '8QRoHR5y84Ag0VgOYx6eVsELVg6OlzE0sO4gf0qkwFI'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings: Settings = Settings()
