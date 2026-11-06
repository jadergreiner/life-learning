"""Verifica a conectividade com o PostgreSQL configurado no lab01."""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.database.connection import get_session


def main() -> int:
    try:
        with get_session() as session:
            result = session.execute(
                text("SELECT 1 AS connected, current_database() AS database_name")
            ).one()

        print(
            "Conexão com o banco estabelecida: "
            f"{result.database_name} (SELECT {result.connected})."
        )
        return 0
    except SQLAlchemyError as error:
        print(f"Falha ao conectar ou consultar o PostgreSQL: {error.__class__.__name__}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
