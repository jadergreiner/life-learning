"""Criação e ciclo de vida das conexões com o PostgreSQL."""

from contextlib import contextmanager
from functools import lru_cache
from typing import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config.settings import get_database_settings


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Retorna o engine compartilhado, configurado pelo settings do lab."""
    settings = get_database_settings()
    return create_engine(
        settings.url,
        echo=settings.echo,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
        pool_timeout=settings.pool_timeout,
        pool_pre_ping=True,
    )


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
    """Cria uma fábrica de sessões vinculada ao engine compartilhado."""
    return sessionmaker(bind=get_engine(), expire_on_commit=False)


@contextmanager
def get_session() -> Iterator[Session]:
    """Abre uma sessão transacional e garante commit ou rollback."""
    with get_session_factory().begin() as session:
        yield session


def dispose_database() -> None:
    """Fecha conexões do pool e limpa os recursos em cache."""
    if get_engine.cache_info().currsize:
        get_engine().dispose()
    get_session_factory.cache_clear()
    get_engine.cache_clear()
