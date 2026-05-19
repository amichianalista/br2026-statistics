from __future__ import annotations

import base64
import html
from functools import lru_cache
from typing import Any

from .supabase_client import get_supabase_client


def is_absolute_asset_url(value: str) -> bool:
    normalized = value.lower()
    return normalized.startswith(("http://", "https://", "data:"))


@lru_cache(maxsize=2048)
def build_public_storage_url(bucket_name: str, asset_path: str) -> str:
    return get_supabase_client().storage.from_(bucket_name).get_public_url(asset_path)


def build_asset_placeholder(label: str, background: str, foreground: str) -> str:
    safe_label = "".join(part[:1] for part in label.split()[:2]).upper() or "?"
    svg = f"""
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 320">
            <rect width="320" height="320" rx="36" fill="{html.escape(background)}" />
            <text
                x="50%"
                y="54%"
                text-anchor="middle"
                font-family="Arial, sans-serif"
                font-size="128"
                font-weight="700"
                fill="{html.escape(foreground)}"
            >
                {html.escape(safe_label)}
            </text>
        </svg>
    """.strip()
    encoded = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


def resolve_asset_url(
    value: Any,
    bucket_name: str | None,
    fallback_label: str,
    fallback_background: str,
    fallback_foreground: str,
) -> str:
    if isinstance(value, str):
        candidate = value.strip()
        if candidate:
            if is_absolute_asset_url(candidate):
                return candidate
            if bucket_name:
                return build_public_storage_url(bucket_name, candidate.lstrip("/"))

    return build_asset_placeholder(
        label=fallback_label,
        background=fallback_background,
        foreground=fallback_foreground,
    )

