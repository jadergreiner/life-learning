# Arquivo de configuração para conectar ao banco de dados
from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Configurações de conexão com o banco de dados."""

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    driver: str = "postgresql+psycopg"
    host: str = "localhost"
    port: int = 5432
    user: str = "pipeline"
    password: str = "pipeline"
    name: str = "pipeline_financeiro"

    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30

    @property
    def url(self) -> str:
        """Monta a URL de conexão do SQLAlchemy."""
        user = quote_plus(self.user)
        password = quote_plus(self.password)
        return f"{self.driver}://{user}:{password}@{self.host}:{self.port}/{self.name}"


@lru_cache
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


database_settings = get_database_settings()
