import pathlib

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
STATIC_DIR = BASE_DIR / "static"
REPORTS_DIR = BASE_DIR / "reports"


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=BASE_DIR.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_name: str
    api_protocol: str
    api_host: str = "localhost"
    api_port: int = 8000
    secret_key_length: int
    algorithm: str
    sqlalchemy_database_url_sync: str
    sqlalchemy_database_url_async: str
    redis_host: str
    redis_port: int
    redis_password: str
    redis_url: str
    redis_expire: int
    redis_db_for_rate_limiter: int
    redis_db_for_objects: int
    redis_db_for_apscheduler: int
    rate_limiter_times: int
    rate_limiter_seconds: int
    mail_server: str
    mail_port: int
    mail_username: str
    mail_password: str
    mail_from: str
    mail_from_name: str
    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    tensorflow_container_name: str
    tensorflow_port: int
    test: bool


settings = Settings()
