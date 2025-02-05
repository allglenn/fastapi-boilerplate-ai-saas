from datetime import timedelta
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    
    
    # Application settings
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    APP_NAME: str = "Your App"  # Default app name
    
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
    
    # Domain name
    DOMAIN_NAME: str = "http://localhost:3000"  # Default for local development
    
    # SMTP settings
    SMTP_HOST: str = "mailcatcher"
    SMTP_PORT: int = 1025
    SENDER_EMAIL: str = "noreply@yourdomain.com"
    
    class Config:
        env_file = ".env"

settings = Settings() 