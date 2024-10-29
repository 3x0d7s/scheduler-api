import os
from dataclasses import dataclass

from sqlalchemy.engine.url import URL


@dataclass
class DbConfig:
    """
    Database configuration class.
    This class holds the settings for the database, such as host, password, port, etc.

    Attributes
    ----------
    host : str
        The host where the database server is located.
    password : str
        The password used to authenticate with the database.
    user : str
        The username used to authenticate with the database.
    name : str
        The name of the database.
    port : int
        The port where the database server is listening.
    echo: bool
        Whether to echo SQL statements to the console.
    """

    host: str
    port: int
    name: str
    user: str
    password: str
    echo: bool

    # For SQLAlchemy
    def construct_sqlalchemy_url(self, driver="asyncpg", host=None, port=None) -> str:
        """
        Constructs and returns a SQLAlchemy URL for this database configuration.
        """

        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.name,
        )
        return uri.render_as_string(hide_password=False)

    @staticmethod
    def from_env(echo: bool = False) -> "DbConfig":
        """
        Creates the DbConfig object from environment variables.
        """
        from dotenv import load_dotenv

        load_dotenv()

        host = os.environ.get("DB_HOST")
        password = os.environ.get("DB_PASSWORD")
        user = os.environ.get("DB_USER")
        name = os.environ.get("DB_NAME")
        port = os.environ.get("DB_PORT", 5432)
        return DbConfig(
            host=host, password=password, user=user, name=name, port=port, echo=echo
        )
