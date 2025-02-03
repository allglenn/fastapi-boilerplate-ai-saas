from datetime import timedelta
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    
    # Albert AI settings
    ALBERT_AI_BASE_URL: str
    ALBERT_AI_API_KEY: str
    
    # Application settings
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1000
    
    # PostgreSQL settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    
    class Config:
        env_file = ".env"

settings = Settings() 