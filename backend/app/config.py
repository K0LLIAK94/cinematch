from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/cinematch"
    tmdb_api_key: str = ""
    tmdb_base_url: str = "https://api.themoviedb.org/3"
    cache_ttl_minutes: int = 720

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
