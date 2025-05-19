import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings configuration using Pydantic BaseSettings.
    Values can be overridden with environment variables.
    """
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", 
        "postgresql://postgres:postgres@localhost:5432/agir"
    )
    
    class Config:
        env_file = ".env"
        extra = "allow"
        case_sensitive = True


settings = Settings() 