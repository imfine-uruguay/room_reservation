from core.config.config_manager import ConfigManager
from core.logging.logger import setup_logger
from utils.database.models import Base, RoomModel
from utils.database.session import SessionLocal, engine

logger = setup_logger(__name__)


def init_db() -> None:
    """Creates the tables (if missing) and seeds the fixed set of rooms."""
    Base.metadata.create_all(bind=engine)

    rooms_config = ConfigManager.get("call_agent.rooms", []) or []
    with SessionLocal() as session:
        for room in rooms_config:
            existing = session.get(RoomModel, room["code"])
            if existing is None:
                session.add(RoomModel(code=room["code"], capacity=room["capacity"]))
                logger.info(f"Seeded room {room['code']} (capacity={room['capacity']})")
            else:
                existing.capacity = room["capacity"]
        session.commit()
