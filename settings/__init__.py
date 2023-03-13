from pydantic import BaseSettings


class Settings(BaseSettings):
    PGSTRING: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
