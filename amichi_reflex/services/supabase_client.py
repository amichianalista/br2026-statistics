from __future__ import annotations

from functools import lru_cache

from supabase import Client, create_client

from .config import get_config, get_supabase_key


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    supabase_url = get_config("SUPABASE_URL")
    supabase_key = get_supabase_key()

    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL ou chave nao configurados.")

    return create_client(supabase_url, supabase_key)

