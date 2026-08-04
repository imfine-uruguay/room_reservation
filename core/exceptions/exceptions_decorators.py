import functools
from collections.abc import Callable
from typing import Any
from urllib.error import HTTPError, URLError

from core.logging.logger import setup_logger

logger = setup_logger(__name__)


def handle_service_exceptions(logger):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            
            except FileNotFoundError as e:
                logger.error(f"Archivo no encontrado en {func.__name__}: {e}")
                raise RuntimeError(f"Archivo no encontrado: {e}")
            
            except HTTPError as e:
                error_body = e.read().decode("utf-8") if hasattr(e, "read") else ""
                logger.error(f"HTTPError {e.code} en {func.__name__}. Body: {error_body}")
                raise RuntimeError(f"Error HTTP {e.code}: {error_body}")
            
            except URLError as e:
                logger.exception(f"URLError en {func.__name__}. Razon: {e.reason}")
                raise RuntimeError(f"Error de conexion: {e.reason}")
            
            except ConnectionError as e:
                logger.exception(f"Error de conexion en {func.__name__}")
                raise RuntimeError(f"Error de conexion: {e}")
            
            except TimeoutError as e:
                logger.exception(f"Timeout en {func.__name__}")
                raise RuntimeError(f"Timeout de conexion: {e}")
            
            except ValueError as e:
                logger.error(f"ValueError en {func.__name__}: {e}")
                raise RuntimeError(f"Error de validacion: {e}")
            
            except RuntimeError:
                raise
            
            except (SystemExit, KeyboardInterrupt, GeneratorExit) as e:
                logger.critical(f"System exception {type(e).__name__} intercepted in service {func.__name__}")
                raise
            
            except Exception as e:
                logger.exception(f"Error inesperado en {func.__name__}")
                raise RuntimeError(f"Error inesperado: {e}")
        
        return wrapper
    return decorator