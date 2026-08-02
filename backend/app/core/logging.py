import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


def create_logger(name: str, filename: str) -> logging.Logger:
    """
    Creates and returns a configured logger safely for cloud containers.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        file_handler = RotatingFileHandler(
            log_dir / filename,
            maxBytes=5 * 1024 * 1024,
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        # Cloud containers (e.g. AppSail) may have restricted or read-only filesystems
        pass

    return logger


app_logger = create_logger("app", "app.log")

api_logger = create_logger("api", "api.log")

error_logger = create_logger("error", "error.log")

auth_logger = create_logger("auth", "auth.log")

ai_logger = create_logger("ai", "ai.log")

case_logger = create_logger("case", "case.log")

complainant_logger = create_logger("complainant", "complainant.log")