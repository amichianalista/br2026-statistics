from __future__ import annotations

from datetime import date, datetime
from typing import Any


def calculate_age(birth_date: date | None) -> int | None:
    if birth_date is None:
        return None

    today = date.today()
    years = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        years -= 1
    return years


def ensure_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return []


def parse_date_value(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        candidate = value.strip()
        if not candidate:
            return None
        try:
            return date.fromisoformat(candidate)
        except ValueError:
            try:
                return datetime.fromisoformat(candidate.replace("Z", "+00:00")).date()
            except ValueError:
                return None
    return None


def parse_datetime_value(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, str):
        candidate = value.strip()
        if not candidate:
            return None
        try:
            return datetime.fromisoformat(candidate.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def format_birth_date(value: date | None) -> str:
    parsed_value = parse_date_value(value)
    if parsed_value is None:
        return "Nao informado"
    return parsed_value.strftime("%d/%m/%Y")


def format_capture(value: datetime | None) -> str:
    parsed_value = parse_datetime_value(value)
    if parsed_value is None:
        return "Nao informado"
    return parsed_value.strftime("%d/%m/%Y as %H:%M")

