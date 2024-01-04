from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from src.utils import obj_from_text


class MissingPasswordException(Exception):
    ...


class DBClient:
    def __init__(
            self,
            host: str,
            port: str,
            database: str,
            user: str,
            password: str = None,
            secret_manager = None, # TODO: protocol for secret manager
            dialect: str = "postgresql"
            ):
        
        self._host = host
        self._port = port
        self._database = database
        self._user = user
        self._dialect = dialect

        if password:
            self._password = password
        elif not password and not secret_manager:
            raise MissingPasswordException(
                "Either a password or secret manager must be provided."
            )
        else:
            self._password = self._get_password(secret_manager)

        self._engine = self._get_engine()

    @classmethod
    def from_config(cls, config: dict) -> DBClient:

        db_conf = config["database"]

        secret_mgr_txt = db_conf.get("secret_manager")
        secret_manager = obj_from_text(secret_mgr_txt) if secret_mgr_txt else None

        return DBClient(
            host=db_conf["host"],
            port=db_conf["port"],
            database=db_conf["database"],
            user=db_conf["user"],
            password=db_conf.get("password"),
            secret_manager=secret_manager,
        )
    
    @staticmethod
    def _get_password(secret_manager, key: str) -> str:
        return secret_manager.get_secret(key)
    
    @property
    def db_exists(self) -> bool:
        return database_exists(self.engine.url)
    
    @property
    def engine(self):
        return self._engine
    
    def create_database(self) -> None:
        if not self.db_exists:
            create_database(self.engine.url)

    def _get_engine(self, echo: bool = False):
        return create_engine(
            "{dialect}://{user}:{password}@{host}:{port}/{database}".format(
                dialect=self._dialect,
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port,
                database=self._database
            ),
            echo=echo
            )
        
