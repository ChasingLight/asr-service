import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):

    # redis
    redis_host: str
    redis_port: int
    redis_password: str
    redis_db_broker: int
    redis_db_result_backend: int

    redis_result_expire_seconds: int

    # fastapi port
    app_port: str

    # current asr strategy
    asr_strategy: str = "l20"

    # l20 asr
    l20_url: str

    # xjtu asr
    xjtu_url: str
    xjtu_api_key: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')

settings = Settings()