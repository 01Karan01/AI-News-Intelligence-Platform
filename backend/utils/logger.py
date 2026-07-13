import logging
import sys
from pathlib import Path

# Use absolute path relative to backend/ so logs always go to the right place
_BACKEND_DIR = Path(__file__).resolve().parent.parent
_LOG_DIR = _BACKEND_DIR / "logs"
_LOG_DIR.mkdir(parents=True, exist_ok=True)

# Create a named logger (avoids mutating the root logger)
logger = logging.getLogger("news_intelligence")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers when module is re-imported
if not logger.handlers:
    # File handler — persistent log
    file_handler = logging.FileHandler(_LOG_DIR / "project.log", mode="a", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(file_handler)

    # Console handler — real-time feedback
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(console_handler)