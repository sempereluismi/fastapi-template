from pydantic_settings import BaseSettings


class Config(BaseSettings):
    APP_NAME: str = "FastAPI Template"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"


config = Config()
