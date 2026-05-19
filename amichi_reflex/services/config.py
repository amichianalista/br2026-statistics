from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any


CURRENT_SEASON = 2026
APP_TITLE = "Amichi Score"
APP_SUBTITLE = "Brasileirao 2026"
ROOT_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT_DIR / "assets"
BACKGROUND_PATH = ASSETS_DIR / "background.png"


@lru_cache(maxsize=1)
def load_env_file() -> dict[str, str]:
    env_path = ROOT_DIR / ".env"
    values: dict[str, str] = {}

    if not env_path.exists():
        return values

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()

    return values


def get_config(name: str, fallback: str | None = None) -> str | None:
    return (
        os.getenv(name)
        or load_env_file().get(name)
        or fallback
    )


def get_supabase_key() -> str | None:
    return get_config("SUPABASE_SECRET_KEY")


def get_supabase_schema() -> str:
    return get_config("SUPABASE_SCHEMA", "public") or "public"


def get_team_bucket() -> str | None:
    return get_config("SUPABASE_BUCKET_TEAMS")


def get_player_bucket() -> str | None:
    return get_config("SUPABASE_BUCKET_PLAYERS")


def get_missing_supabase_settings() -> list[str]:
    missing_fields: list[str] = []
    if not get_config("SUPABASE_URL"):
        missing_fields.append("SUPABASE_URL")
    if not get_supabase_key():
        missing_fields.append("SUPABASE_SECRET_KEY")
    return missing_fields


def has_supabase_config() -> bool:
    return not get_missing_supabase_settings()


def asset_url(relative_path: str) -> str:
    return f"/{relative_path.lstrip('/')}"


def app_meta() -> dict[str, Any]:
    return {
        "title": f"{APP_TITLE} | {APP_SUBTITLE}",
        "description": (
            "Leitura visual de elencos, perfis e versatilidade posicional "
            "do Brasileirao 2026."
        ),
    }
