"""Ponto de entrada para processar um evento JSON pela linha de comando."""

import argparse
import json
import sys
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

from src.database.connection import dispose_database
from src.database.errors import DatabaseError
from src.domain.events import EventConflictError, EventValidationError
from src.repositories.accounts import AccountNotFoundError
from src.services.event_processor import EventProcessor


def main() -> int:
    parser = argparse.ArgumentParser(description="Processa um evento financeiro JSON.")
    parser.add_argument("payload", help="JSON do evento ou caminho para arquivo JSON")
    args = parser.parse_args()

    try:
        candidate = Path(args.payload)
        raw = candidate.read_text(encoding="utf-8") if candidate.is_file() else args.payload
        result = EventProcessor().process_event(json.loads(raw))
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (
        json.JSONDecodeError,
        OSError,
        EventValidationError,
        EventConflictError,
        AccountNotFoundError,
    ) as error:
        print(f"Evento não processado: {error}", file=sys.stderr)
        return 2
    except (DatabaseError, SQLAlchemyError) as error:
        print(f"Falha de persistência: {error.__class__.__name__}", file=sys.stderr)
        return 1
    finally:
        dispose_database()


if __name__ == "__main__":
    raise SystemExit(main())
