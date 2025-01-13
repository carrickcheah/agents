from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    aws_access_key_id: str
    aws_secret_access_key: str
    opeanai_api_key: str
    qdrant_host: str


config = Settings()





