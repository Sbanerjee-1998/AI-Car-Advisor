from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect


def test_initial_migration_creates_all_tables(tmp_path):
    database = tmp_path / "migration.db"
    config = Config(str(Path("backend/alembic.ini")))
    config.set_main_option("sqlalchemy.url", f"sqlite:///{database}")
    command.upgrade(config, "head")
    tables = set(inspect(create_engine(f"sqlite:///{database}")).get_table_names())
    assert {"users", "auth_sessions", "conversations", "messages", "conversation_preferences", "favourites", "alembic_version"} <= tables
