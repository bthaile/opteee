"""
Database initialization helpers.
"""

from app.db.database import Base, engine
from app.db import models  # noqa: F401 - ensure model metadata is registered


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

