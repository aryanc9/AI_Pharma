import os
from pathlib import Path
from typing import Literal


# -------------------------------------------------------------------
# Environment
# -------------------------------------------------------------------

ENV: Literal["dev", "prod"] = os.getenv("APP_ENV", "dev")


# -------------------------------------------------------------------
# Base Paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "pharmacy.db"))


# -------------------------------------------------------------------
# Database
# -------------------------------------------------------------------

DATABASE_URL = f"sqlite:///{DB_PATH}"


# -------------------------------------------------------------------
# LLM Configuration
# -------------------------------------------------------------------

LLM_PROVIDER: Literal["ollama", "gemini"] = os.getenv(
    "LLM_PROVIDER", "ollama"
)

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# Gemini (future-ready, optional)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# -------------------------------------------------------------------
# Scheduler
# -------------------------------------------------------------------

REFILL_INTERVAL_SECONDS = int(
    os.getenv("REFILL_INTERVAL_SECONDS", "60")
)


# -------------------------------------------------------------------
# Observability
# -------------------------------------------------------------------

ENABLE_DECISION_TRACE = os.getenv(
    "ENABLE_DECISION_TRACE", "true"
).lower() == "true"


# --------------------
