from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@127.0.0.1:5433/civicpulse"
    REDIS_URL: str = "redis://127.0.0.1:6379/0"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
