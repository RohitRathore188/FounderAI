from typing import Generator, Any
from app.core.logging import logger

class DatabaseConnectionStub:
    """Skeleton Database Connection class for future SQL/NoSQL DB storage."""
    def __init__(self):
        self.connected = False

    def connect(self) -> None:
        logger.info("Database: Connecting to persistent data store...")
        self.connected = True

    def disconnect(self) -> None:
        logger.info("Database: Disconnecting from persistent data store...")
        self.connected = False

db_connection = DatabaseConnectionStub()

def get_db_session() -> Generator[Any, None, None]:
    """Dependency Injection session provider stub."""
    db_connection.connect()
    try:
        yield db_connection
    finally:
        db_connection.disconnect()
