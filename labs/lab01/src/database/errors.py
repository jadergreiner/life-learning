"""Exceções de infraestrutura do banco de dados."""


class DatabaseError(RuntimeError):
    """Erro base de acesso ao banco."""


class DatabaseConnectionError(DatabaseError):
    """Falha ao obter ou manter conexão com o banco."""


class QueryExecutionError(DatabaseError):
    """Falha ao executar uma consulta no banco."""
