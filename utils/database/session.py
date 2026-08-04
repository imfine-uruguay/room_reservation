from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config.config_manager import ConfigManager

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def build_engine():
    db_path = ConfigManager.get_sqlite_db_path()
    full_path = (_PROJECT_ROOT / db_path).resolve()
    full_path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{full_path}", connect_args={"check_same_thread": False})


engine = build_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
