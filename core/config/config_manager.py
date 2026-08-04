import os
from pathlib import Path

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logging.logger import setup_logger

logger = setup_logger(__name__)

_PROJECT_ROOT = Path(__file__).parent.parent.parent


class _EnvSettings(BaseSettings):
    DB_ENGINE: str
    SQLITE_DB_PATH: str

    LLM_MODEL_IN_GROP: str
    LLM_MODEL_URL:  str
    LLM_MODEL_TEMPERATURE: float
    LLM_MODEL_PROVIDER: str
    LLM_MODEL_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=str(_PROJECT_ROOT / ".env"),
        case_sensitive=True,
        extra="ignore",
    )


_env = _EnvSettings()


class ConfigManager:
    _instance: "ConfigManager | None" = None
    _config: dict | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def _load_config(self, config_path: str | None = None):
        if config_path is None:
            config_path = os.getenv("CONFIG_PATH", str(Path(__file__).parent / "config.yaml"))
        logger.info(f"Loading configuration from: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

    def _get_config(self) -> dict:
        if self._config is None:
            self._load_config()
        return self._config


    @classmethod
    def _inst(cls) -> "ConfigManager":
        return cls()

    @classmethod
    def load_config(cls, config_path: str | None = None) -> None:
        cls._inst()._load_config(config_path)

    @classmethod
    def get_config(cls) -> dict:
        return cls._inst()._get_config()

    @classmethod
    def get(cls, key, default=None):
        config = cls.get_config()
        parts = key.split(".")
        val = config
        for part in parts:
            if isinstance(val, dict) and part in val:
                val = val[part]
            else:
                return default
        return val


    @classmethod
    def get_db_engine(cls) -> str:
        return _env.DB_ENGINE

    @classmethod
    def get_sqlite_db_path(cls) -> str:
        return _env.SQLITE_DB_PATH


    @classmethod
    def get_llm_model_name_in_grop(cls) -> str:
        return _env.LLM_MODEL_IN_GROP

    @classmethod
    def get_llm_model_url(cls) -> str:
        return _env.LLM_MODEL_URL

    @classmethod
    def get_llm_model_temperature(cls) -> float:
        return _env.LLM_MODEL_TEMPERATURE
    
    @classmethod
    def get_llm_model_provider(cls) -> str:
        return _env.LLM_MODEL_PROVIDER
    
    @classmethod
    def get_llm_model_api_key(cls) -> str:
        return _env.LLM_MODEL_API_KEY
