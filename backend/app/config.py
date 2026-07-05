from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    github_client_id: str
    github_client_secret: str
    database_url: str

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
