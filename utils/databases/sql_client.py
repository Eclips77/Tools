
from typing import Any, Dict, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Connection

class SQLClient:
    """Generic SQL client using SQLAlchemy for connections and raw execution."""

    def __init__(self, db_url: str) -> None:
        """
        Initialize SQL client.
        Args:
            db_url: SQLAlchemy database URL (e.g., sqlite:///file.db).
        """
        self.engine: Engine = create_engine(db_url, future=True)

    def connect(self) -> Connection:
        """Return a new connection."""
        return self.engine.connect()

    def execute(self, sql: str, params: Optional[Dict[str, Any]] = None) -> None:
        """Execute a raw SQL statement."""
        with self.connect() as conn:
            conn.execute(text(sql), params or {})
            conn.commit()

    def fetchall(self, sql: str, params: Optional[Dict[str, Any]] = None):
        """Execute a query and fetch all rows."""
        with self.connect() as conn:
            result = conn.execute(text(sql), params or {})
            return result.fetchall()

def main() -> None:
    client = SQLClient("sqlite:///test.db")
    client.execute("CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, name TEXT)")
    client.execute("INSERT INTO items(name) VALUES (:n)", {"n": "alpha"})
    print(client.fetchall("SELECT * FROM items", {}))

if __name__ == "__main__":
    main()
