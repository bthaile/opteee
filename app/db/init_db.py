"""
Database initialization helpers.
"""

from app.db.database import Base, engine, DATABASE_URL
from app.db import models  # noqa: F401 - ensure model metadata is registered


def init_db() -> None:
    # Log which DB we're using (mask password)
    _url = DATABASE_URL
    if "@" in _url and "postgresql" in _url:
        _masked = _url.split("@")[1] if "@" in _url else _url
        print(f"📦 Database: Postgres @ {_masked}")
    else:
        print(f"📦 Database: SQLite ({_url})")
    Base.metadata.create_all(bind=engine)

