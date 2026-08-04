import logging
import os
import time
from pathlib import Path

from dotenv import dotenv_values

from utils.timestamps import utc_date

# ── Helpers ───────────────────────────────────────────────────────────────────
_LOG_ENABLED = (os.environ.get("LOG_ENABLED") or "true").lower() != "false"
_LOG_STDOUT  = (os.environ.get("LOG_STDOUT") or "false").lower() == "true"

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class _DailyFileHandler(logging.Handler):

    def __init__(self, base_path: Path, prefix: str, backup_count: int = 7, ext: str = ".log") -> None:
        super().__init__()
        self._base_path   = base_path
        self._prefix      = prefix
        self._backup_count = backup_count
        self._ext          = ext
        self._current_date: str | None = None
        self._fh: logging.FileHandler | None = None
        self._rotate_to_today()

    def _today(self) -> str:
        return utc_date()

    def _rotate_to_today(self) -> None:
        if self._fh:
            self._fh.close()
        today = self._today()
        self._current_date = today
        log_file = self._base_path / f"{self._prefix}_{today}{self._ext}"
        self._fh = logging.FileHandler(str(log_file), encoding="utf-8", delay=False)
        if self.formatter:
            self._fh.setFormatter(self.formatter)
        self._purge_old_files()

    def _purge_old_files(self) -> None:
        files = sorted(self._base_path.glob(f"{self._prefix}_????-??-??{self._ext}"))
        for old in files[: max(0, len(files) - self._backup_count)]:
            try:
                old.unlink()
            except OSError:
                pass

    def setFormatter(self, fmt: logging.Formatter) -> None:
        super().setFormatter(fmt)
        if self._fh:
            self._fh.setFormatter(fmt)

    def emit(self, record: logging.LogRecord) -> None:
        if self._today() != self._current_date:
            self._rotate_to_today()
        if self._fh:
            self._fh.emit(record)

    def close(self) -> None:
        if self._fh:
            self._fh.close()
        super().close()



def _resolve_log_dir() -> str | None:
    value = os.environ.get("LOG_DIR")
    if value:
        return value

    env_file = _PROJECT_ROOT / ".env"
    if env_file.exists():
        try:
            
            return dotenv_values(str(env_file)).get("LOG_DIR") or None
        except (OSError, ValueError):
            return None
    return None


def _log_base_path() -> Path:
    log_dir = _resolve_log_dir()
    path = Path(log_dir) if log_dir else _PROJECT_ROOT / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def setup_logger(
    name: str = __name__,
    log_dir: str = "logger",
    level: int = logging.DEBUG,
) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    if not _LOG_ENABLED:
        logger.addHandler(logging.NullHandler())
        return logger

    log_path = _log_base_path()

    fmt = logging.Formatter(
        "%(asctime)s  %(levelname)-7s  %(name)s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fmt.converter = time.gmtime

    info_handler = _DailyFileHandler(log_path, prefix="info", backup_count=7)
    info_handler.setLevel(logging.DEBUG)
    info_handler.addFilter(lambda record: record.levelno < logging.ERROR)
    info_handler.setFormatter(fmt)
    logger.addHandler(info_handler)

    error_handler = _DailyFileHandler(log_path, prefix="error", backup_count=7)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(fmt)
    logger.addHandler(error_handler)

    #only log to console if LOG_STDOUT is true
    if _LOG_STDOUT:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter("%(levelname)s  %(name)s  %(message)s")
        )
        logger.addHandler(console_handler)

    return logger
