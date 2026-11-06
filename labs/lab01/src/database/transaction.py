"""Unidade de trabalho que agrupa consultas numa única transação."""

from contextlib import AbstractContextManager
from types import TracebackType
from typing import Self

from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.database.connection import get_session_factory
from src.database.errors import DatabaseConnectionError, QueryExecutionError
from src.repositories.accounts import AccountsRepository
from src.repositories.inbound_events import InboundEventsRepository
from src.repositories.transactions import TransactionsRepository


class UnitOfWork(AbstractContextManager["UnitOfWork"]):
    def __init__(self) -> None:
        self.session: Session | None = None
        self.accounts: AccountsRepository
        self.inbound_events: InboundEventsRepository
        self.transactions: TransactionsRepository
        self._session_context = None

    def __enter__(self) -> Self:
        self._session_context = get_session_factory().begin()
        try:
            self.session = self._session_context.__enter__()
        except OperationalError as error:
            raise DatabaseConnectionError("Não foi possível conectar ao PostgreSQL.") from error
        self.accounts = AccountsRepository(self.session)
        self.inbound_events = InboundEventsRepository(self.session)
        self.transactions = TransactionsRepository(self.session)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        assert self._session_context is not None
        try:
            result = self._session_context.__exit__(exc_type, exc_value, traceback)
        except OperationalError as error:
            raise DatabaseConnectionError("Falha de conexão durante a transação.") from error
        except SQLAlchemyError as error:
            raise QueryExecutionError("Falha ao executar a transação no PostgreSQL.") from error
        finally:
            self.session = None
        if isinstance(exc_value, OperationalError):
            raise DatabaseConnectionError("Falha de conexão durante a operação.") from exc_value
        if isinstance(exc_value, SQLAlchemyError):
            raise QueryExecutionError("Falha ao executar a operação no PostgreSQL.") from exc_value
        return result
