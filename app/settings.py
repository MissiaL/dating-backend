from logging import getLogger
from pathlib import Path

from pydantic import BaseSettings, ValidationError
from dotenv import load_dotenv

# Read settings from .env file in local dev environment
load_dotenv()


class Settings(BaseSettings):
    # App instance
    app_uri: str = 'https'
    app_name: str = 'Dating Backend'
    app_host: str = '0.0.0.0'
    app_port: int = 4000

    # Environment settings
    env_name: str = 'development'
    debug: bool = True
    sync_db: bool = True  # indicate synchronous mode for database
    timezone: str = 'Europe/Moscow'

    # Database
    postgres_host: str = 'localhost'
    postgres_port: str = 5432
    postgres_db: str = 'dating'
    postgres_username: str = 'dating'
    postgres_password: str = 'dating'
    postgres_max_conn: int = 2

    #cors
    cors_allow_origins = 'http://dating-web-develop.hackecosystem.dev2.k8s.tcsbank.ru,http://localhost:3000,http://127.0.0.1:3000,https://dating-web-develop.hackecosystem.dev2.k8s.tcsbank.ru,http://dating-web.hackecosystem.dev2.k8s.tcsbank.ru,https://dating-web.hackecosystem.dev2.k8s.tcsbank.ru'

    # images_storage
    image_storage_name = 'images'

    @property
    def project_dir(self):
        return Path(__file__).parent.parent.absolute()

    @property
    def images_dir(self):
        return Path(self.project_dir, self.image_storage_name).absolute()

    # Logging
    log_sql_queries: bool = False

    class Config:
        env_prefix = ''
        case_insensitive = True


try:
    settings = Settings()
except ValidationError as err:
    logger = getLogger(__name__)
    logger.error('App configuration failed')
    for error in err.errors():
        var = error['loc'][0].upper()
        msg = error['msg']
        logger.error(f'Bad variable {var}: {msg}')
    raise SystemExit(1)
