from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Define application settings loaded from environment variables.

    Attributes
    ----------
    app_name : str
        Name of the application.
    app_version : str
        Current version of the application.
    debug : bool
        Enable debug mode.
    db_host : str
        Database host address.
    db_port : int
        Database port number.
    db_user : str
        Database username.
    db_password : str
        Database password.
    db_name : str
        Database name.

    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = "Globant DE Tech API"
    app_version: str = "0.1.0"
    debug: bool = False

    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "globant_de"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings instance.

    Returns
    -------
    Settings
        The application settings loaded from environment variables.

    """
    return Settings()
