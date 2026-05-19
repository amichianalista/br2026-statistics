from __future__ import annotations

from functools import lru_cache
from typing import Any

from .assets import resolve_asset_url
from .config import CURRENT_SEASON, get_player_bucket, get_supabase_schema, get_team_bucket
from .formatters import (
    calculate_age,
    ensure_list,
    format_birth_date,
    format_capture,
    parse_date_value,
    parse_datetime_value,
)
from .supabase_client import get_supabase_client


PlayerRow = dict[str, Any]


def build_versatility_label(alternative_positions: list[str]) -> str:
    if not alternative_positions:
        return "Especialista"
    if len(alternative_positions) == 1:
        return "Hibrido"
    return "Versatil"


def normalize_player(row: PlayerRow) -> PlayerRow:
    positions = ensure_list(row.get("posicoes_detalhadas"))
    main_position = (
        row.get("posicao_detalhada_principal")
        or row.get("posicao_principal")
        or "Posicao nao definida"
    )
    alternate_positions = [position for position in positions if position != main_position]
    team_name = row.get("nome_curto_time") or row.get("nome_time") or "Time indefinido"
    birth_date = parse_date_value(row.get("data_nascimento"))
    captured_at = parse_datetime_value(row.get("capturado_em_utc"))
    age = calculate_age(birth_date)
    age_display = f"{age} anos" if age is not None else "Idade indisponivel"
    shirt_number = str(row.get("numero_camisa") or "--")
    team_primary = row.get("cor_primaria_time") or "#0F1722"
    team_secondary = row.get("cor_secundaria_time") or "#73859B"
    team_text = row.get("cor_texto_time") or "#F7FBFD"
    resolved_team_crest = resolve_asset_url(
        value=row.get("url_escudo_time"),
        bucket_name=get_team_bucket(),
        fallback_label=team_name,
        fallback_background=team_primary,
        fallback_foreground=team_text,
    )
    resolved_player_photo = resolve_asset_url(
        value=row.get("url_foto_jogador"),
        bucket_name=get_player_bucket(),
        fallback_label=row.get("nome_jogador") or "Jogador",
        fallback_background=team_secondary,
        fallback_foreground=team_text,
    )
    nationality = row.get("nacionalidade") or "Nao informado"
    competition = row.get("competicao") or "Campeonato nao informado"
    player_name = row.get("nome_jogador") or "Jogador sem nome"
    versatility_label = build_versatility_label(alternate_positions)
    summary = f"{team_name} | {main_position} | {age_display}"
    executive_summary = (
        f"{player_name} aparece no recorte do Brasileirao 2026 defendendo o {team_name}, "
        f"com funcao principal de {main_position.lower()} e perfil de uso {versatility_label.lower()}."
    )
    profile_note = (
        f"Leitura inicial de elenco: {player_name} combina identidade competitiva, "
        f"contexto de clube e interpretacao posicional em uma ficha de consulta rapida."
    )
    search_blob = " ".join(
        [
            str(player_name),
            str(team_name),
            str(main_position),
            str(nationality),
            " ".join(positions),
        ]
    ).lower()

    return {
        **row,
        "idade": age,
        "idade_display": age_display,
        "birth_date_display": format_birth_date(birth_date),
        "captured_at_display": format_capture(captured_at),
        "sigla_display": row.get("sigla_time") or "--",
        "posicao_principal_display": row.get("posicao_principal") or "--",
        "temporada_display": str(row.get("temporada") or "--"),
        "posicoes_detalhadas_list": positions,
        "posicoes_alternativas": alternate_positions,
        "posicao_label": main_position,
        "team_name_display": team_name,
        "shirt_number_display": shirt_number,
        "competicao_display": competition,
        "nacionalidade_display": nationality,
        "versatility_label": versatility_label,
        "alternative_positions_count": len(alternate_positions),
        "team_primary": team_primary,
        "team_secondary": team_secondary,
        "team_text": team_text,
        "team_crest_display_url": resolved_team_crest,
        "player_photo_display_url": resolved_player_photo,
        "hero_summary": summary,
        "executive_summary": executive_summary,
        "profile_note": profile_note,
        "card_gradient": f"linear-gradient(140deg, {team_primary}, {team_secondary})",
        "search_blob": search_blob,
    }


def load_players_from_supabase() -> list[PlayerRow]:
    supabase = get_supabase_client()
    schema = get_supabase_schema()

    players_response = (
        supabase.schema(schema)
        .table("jogadores")
        .select(
            ",".join(
                [
                    "id_jogador",
                    "nome_jogador",
                    "id_time",
                    "temporada",
                    "competicao",
                    "posicao_detalhada_principal",
                    "posicoes_detalhadas",
                    "numero_camisa",
                    "nacionalidade",
                    "data_nascimento",
                    "url_foto_jogador",
                    "capturado_em_utc",
                    "codigo_posicao_detalhada_principal",
                    "posicao_principal",
                    "codigos_posicoes_detalhadas",
                ]
            )
        )
        .eq("temporada", CURRENT_SEASON)
        .execute()
    )

    teams_response = (
        supabase.schema(schema)
        .table("times")
        .select(
            ",".join(
                [
                    "id_time",
                    "temporada",
                    "nome_time",
                    "nome_curto_time",
                    "sigla_time",
                    "cor_primaria_time",
                    "cor_secundaria_time",
                    "cor_texto_time",
                    "url_escudo_time",
                ]
            )
        )
        .eq("temporada", CURRENT_SEASON)
        .execute()
    )

    players_data = players_response.data or []
    teams_data = teams_response.data or []
    teams_by_key = {(team["id_time"], team["temporada"]): team for team in teams_data}

    merged_rows: list[PlayerRow] = []
    for player in players_data:
        if (player.get("posicao_principal") or "") == "revisar":
            continue

        team = teams_by_key.get((player.get("id_time"), player.get("temporada")))
        if not team:
            continue

        merged_rows.append({**player, **team})

    merged_rows.sort(key=lambda row: (str(row.get("nome_time") or ""), str(row.get("nome_jogador") or "")))
    return [normalize_player(row) for row in merged_rows]


@lru_cache(maxsize=1)
def load_players() -> list[PlayerRow]:
    return load_players_from_supabase()


def filter_players(
    players: list[PlayerRow],
    selected_team: str,
    selected_position: str,
    search_term: str,
) -> list[PlayerRow]:
    filtered = players

    if selected_team != "Todos os times":
        filtered = [player for player in filtered if player["team_name_display"] == selected_team]

    if selected_position != "Todas as posicoes":
        filtered = [player for player in filtered if player["posicao_label"] == selected_position]

    normalized_term = search_term.strip().lower()
    if normalized_term:
        filtered = [player for player in filtered if normalized_term in player["search_blob"]]

    return filtered


def build_team_options(players: list[PlayerRow]) -> list[str]:
    return ["Todos os times", *sorted({str(player["team_name_display"]) for player in players})]


def build_position_options(players: list[PlayerRow]) -> list[str]:
    return ["Todas as posicoes", *sorted({str(player["posicao_label"]) for player in players})]
