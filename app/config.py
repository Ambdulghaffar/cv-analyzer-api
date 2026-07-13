from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    supabase_service_role_key: str
    groq_api_key: str
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

settings = Settings()