from __future__ import annotations

import base64
import os
from functools import lru_cache
from datetime import date, datetime
from pathlib import Path
from typing import Any

import psycopg
import streamlit as st
from psycopg.rows import dict_row
from supabase import Client, create_client


SCHEMA = "br_2026"
CURRENT_SEASON = 2026
APP_TITLE = "Amichi Score"
APP_SUBTITLE = "Brasileirao 2026"
ROOT_DIR = Path(__file__).resolve().parent
BACKGROUND_PATH = ROOT_DIR / "assets" / "background.png"


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


@lru_cache(maxsize=1)
def load_streamlit_secrets() -> dict[str, str]:
    try:
        return {key: str(value) for key, value in st.secrets.items()}
    except Exception:
        return {}


def get_config(name: str, fallback: str | None = None) -> str | None:
    secret_values = load_streamlit_secrets()
    file_values = load_env_file()
    return os.getenv(name) or secret_values.get(name) or file_values.get(name) or fallback


def get_supabase_key() -> str | None:
    return get_config("SUPABASE_SECRET_KEY") or get_config("SUPABASE_SERVICE_ROLE_KEY")


def has_supabase_config() -> bool:
    return bool(get_config("SUPABASE_URL") and get_supabase_key())


def has_database_url() -> bool:
    return bool(get_config("DATABASE_URL"))


def get_missing_database_settings() -> list[str]:
    if has_supabase_config():
        return []

    if has_database_url():
        return []

    required_fields = [
        "DATABASE_HOST",
        "DATABASE_PORT",
        "DATABASE_NAME",
        "DATABASE_USER",
        "DATABASE_PASSWORD",
    ]
    return [field for field in required_fields if not get_config(field)]


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    supabase_url = get_config("SUPABASE_URL")
    supabase_key = get_supabase_key()

    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL ou chave nao configurados.")

    return create_client(supabase_url, supabase_key)


def get_connection() -> psycopg.Connection:
    database_url = get_config("DATABASE_URL")
    if database_url:
        return psycopg.connect(database_url, row_factory=dict_row)

    return psycopg.connect(
        host=get_config("DATABASE_HOST"),
        port=get_config("DATABASE_PORT"),
        dbname=get_config("DATABASE_NAME"),
        user=get_config("DATABASE_USER"),
        password=get_config("DATABASE_PASSWORD"),
        sslmode=get_config("DATABASE_SSLMODE", "require"),
        row_factory=dict_row,
    )


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


def format_birth_date(value: date | None) -> str:
    if value is None:
        return "Nao informado"
    return value.strftime("%d/%m/%Y")


def format_capture(value: datetime | None) -> str:
    if value is None:
        return "Nao informado"
    return value.strftime("%d/%m/%Y as %H:%M")


def background_data_uri() -> str:
    if not BACKGROUND_PATH.exists():
        return ""
    encoded = base64.b64encode(BACKGROUND_PATH.read_bytes()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def normalize_player(row: dict[str, Any]) -> dict[str, Any]:
    positions = ensure_list(row.get("posicoes_detalhadas"))
    main_position = row.get("posicao_detalhada_principal") or row.get("posicao_principal") or "Posicao nao definida"
    alternate_positions = [position for position in positions if position != main_position]
    shirt_number = row.get("numero_camisa") or "--"
    team_name = row.get("nome_curto_time") or row.get("nome_time") or "Time indefinido"

    return {
        **row,
        "idade": calculate_age(row.get("data_nascimento")),
        "posicoes_detalhadas_list": positions,
        "posicoes_alternativas": alternate_positions,
        "posicao_label": main_position,
        "team_name_display": team_name,
        "shirt_number_display": shirt_number,
        "competicao_display": row.get("competicao") or "Campeonato nao informado",
        "nacionalidade_display": row.get("nacionalidade") or "Nao informado",
        "team_primary": row.get("cor_primaria_time") or "#101418",
        "team_secondary": row.get("cor_secundaria_time") or "#8ca3b8",
        "team_text": row.get("cor_texto_time") or "#f7fafc",
    }


def load_players_from_supabase() -> list[dict[str, Any]]:
    supabase = get_supabase_client()

    players_response = (
        supabase.schema(SCHEMA)
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
        supabase.schema(SCHEMA)
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

    teams_by_key = {
        (team["id_time"], team["temporada"]): team
        for team in teams_data
    }

    merged_rows: list[dict[str, Any]] = []
    for player in players_data:
        if (player.get("posicao_principal") or "") == "revisar":
            continue

        team = teams_by_key.get((player.get("id_time"), player.get("temporada")))
        if not team:
            continue

        merged_rows.append({**player, **team})

    merged_rows.sort(
        key=lambda row: (
            row.get("nome_time") or "",
            row.get("nome_jogador") or "",
        )
    )
    return [normalize_player(row) for row in merged_rows]


@st.cache_data(ttl=300, show_spinner=False)
def load_players() -> list[dict[str, Any]]:
    if has_supabase_config():
        return load_players_from_supabase()

    query = f"""
        select
            j.id_jogador,
            j.nome_jogador,
            j.id_time,
            j.temporada,
            j.competicao,
            j.posicao_detalhada_principal,
            j.posicoes_detalhadas,
            j.numero_camisa,
            j.nacionalidade,
            j.data_nascimento,
            j.url_foto_jogador,
            j.capturado_em_utc,
            j.codigo_posicao_detalhada_principal,
            j.posicao_principal,
            j.codigos_posicoes_detalhadas,
            t.nome_time,
            t.nome_curto_time,
            t.sigla_time,
            t.cor_primaria_time,
            t.cor_secundaria_time,
            t.cor_texto_time,
            t.url_escudo_time
        from {SCHEMA}.jogadores j
        join {SCHEMA}.times t
          on t.id_time = j.id_time
         and t.temporada = j.temporada
        where j.temporada = %s
          and coalesce(j.posicao_principal, '') <> 'revisar'
        order by t.nome_time, j.nome_jogador
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (CURRENT_SEASON,))
            rows = cur.fetchall()

    return [normalize_player(row) for row in rows]


def inject_styles() -> None:
    bg_uri = background_data_uri()
    st.markdown(
        f"""
        <style>
            :root {{
                --app-bg: #edf3f7;
                --ink-900: #0e1726;
                --ink-700: #415161;
                --ink-500: #6e8295;
                --line-soft: rgba(255, 255, 255, 0.28);
                --surface-strong: rgba(7, 17, 28, 0.72);
                --surface-card: rgba(248, 251, 253, 0.82);
                --surface-card-dark: rgba(13, 24, 38, 0.76);
                --shadow-strong: 0 26px 64px rgba(7, 17, 28, 0.18);
                --shadow-soft: 0 18px 40px rgba(7, 17, 28, 0.10);
                --radius-xl: 28px;
                --radius-lg: 22px;
                --radius-md: 18px;
            }}

            .stApp {{
                background:
                    linear-gradient(180deg, rgba(237, 243, 247, 0.50), rgba(237, 243, 247, 0.92)),
                    url("{bg_uri}") center / cover fixed no-repeat;
                color: var(--ink-900);
            }}

            .stApp::before {{
                content: "";
                position: fixed;
                inset: 0;
                background:
                    radial-gradient(circle at top left, rgba(255, 255, 255, 0.70), transparent 38%),
                    radial-gradient(circle at bottom right, rgba(255, 209, 102, 0.16), transparent 26%);
                pointer-events: none;
                z-index: 0;
            }}

            .main .block-container {{
                max-width: 30rem;
                padding: 1.1rem 1rem 3rem;
                position: relative;
                z-index: 1;
            }}

            #MainMenu, footer, header {{
                visibility: hidden;
            }}

            html, body, [class*="css"] {{
                font-family: Aptos, "Segoe UI", "Trebuchet MS", sans-serif;
            }}

            [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {{
                background: transparent;
            }}

            [data-testid="stSelectbox"] label,
            [data-testid="stSelectbox"] p {{
                color: var(--ink-700);
                font-size: 0.85rem;
                font-weight: 600;
                letter-spacing: 0.03em;
            }}

            div[data-baseweb="select"] > div {{
                min-height: 3.35rem;
                border-radius: 18px;
                border: 1px solid rgba(65, 81, 97, 0.14);
                background: rgba(255, 255, 255, 0.72);
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.48);
            }}

            .top-shell {{
                padding: 1.15rem 1.1rem 1.3rem;
                border-radius: var(--radius-xl);
                background: linear-gradient(145deg, rgba(7, 17, 28, 0.88), rgba(21, 44, 69, 0.72));
                color: #f8fbfd;
                box-shadow: var(--shadow-strong);
                border: 1px solid rgba(255, 255, 255, 0.14);
                backdrop-filter: blur(14px);
            }}

            .top-shell .eyebrow {{
                display: inline-flex;
                margin-bottom: 0.7rem;
                padding: 0.38rem 0.72rem;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.09);
                font-size: 0.73rem;
                font-weight: 700;
                letter-spacing: 0.12em;
                text-transform: uppercase;
            }}

            .top-shell h1 {{
                margin: 0;
                font-family: Georgia, "Times New Roman", serif;
                font-size: 2.1rem;
                line-height: 1.02;
                letter-spacing: -0.03em;
            }}

            .top-shell p {{
                margin: 0.75rem 0 0;
                color: rgba(248, 251, 253, 0.80);
                line-height: 1.45;
                font-size: 0.97rem;
            }}

            .section-title {{
                margin: 1.15rem 0 0.55rem;
                color: var(--ink-500);
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0.14em;
                text-transform: uppercase;
            }}

            .hero-card {{
                position: relative;
                overflow: hidden;
                padding: 1.05rem;
                border-radius: var(--radius-xl);
                background:
                    linear-gradient(160deg, var(--team-primary), var(--team-secondary));
                color: var(--team-text);
                box-shadow: var(--shadow-strong);
                border: 1px solid rgba(255, 255, 255, 0.16);
            }}

            .hero-card::before {{
                content: "";
                position: absolute;
                inset: 0;
                background:
                    linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0)),
                    radial-gradient(circle at top right, rgba(255, 255, 255, 0.18), transparent 32%);
                pointer-events: none;
            }}

            .hero-card-inner {{
                position: relative;
                display: grid;
                grid-template-columns: 1fr;
                gap: 1rem;
            }}

            .hero-topline {{
                display: flex;
                justify-content: space-between;
                gap: 0.8rem;
                align-items: flex-start;
            }}

            .hero-tag {{
                display: inline-flex;
                width: fit-content;
                padding: 0.36rem 0.68rem;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.14);
                backdrop-filter: blur(8px);
                font-size: 0.7rem;
                font-weight: 800;
                letter-spacing: 0.10em;
                text-transform: uppercase;
            }}

            .team-badge {{
                width: 3.1rem;
                height: 3.1rem;
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.14);
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 0.45rem;
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.18);
            }}

            .team-badge img {{
                width: 100%;
                height: 100%;
                object-fit: contain;
            }}

            .player-photo-wrap {{
                display: flex;
                justify-content: center;
                padding-top: 0.2rem;
            }}

            .player-photo-wrap img {{
                width: min(76vw, 18rem);
                max-height: 18rem;
                object-fit: contain;
                filter: drop-shadow(0 18px 32px rgba(0, 0, 0, 0.24));
            }}

            .hero-name {{
                margin: 0.2rem 0 0;
                font-family: Georgia, "Times New Roman", serif;
                font-size: 2rem;
                line-height: 0.98;
                letter-spacing: -0.03em;
            }}

            .hero-subline {{
                margin-top: 0.55rem;
                font-size: 1rem;
                opacity: 0.92;
            }}

            .chip-row {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.45rem;
                margin-top: 0.95rem;
            }}

            .chip {{
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                padding: 0.46rem 0.72rem;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.14);
                backdrop-filter: blur(10px);
                font-size: 0.76rem;
                font-weight: 700;
            }}

            .bio-grid {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.8rem;
                margin-top: 1rem;
            }}

            .info-card {{
                padding: 0.95rem 0.9rem;
                border-radius: var(--radius-lg);
                background: var(--surface-card);
                backdrop-filter: blur(14px);
                box-shadow: var(--shadow-soft);
                border: 1px solid rgba(255, 255, 255, 0.48);
            }}

            .info-card.dark {{
                color: #f8fbfd;
                background: var(--surface-card-dark);
                border: 1px solid rgba(255, 255, 255, 0.12);
            }}

            .info-label {{
                color: var(--ink-500);
                font-size: 0.73rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }}

            .dark .info-label {{
                color: rgba(248, 251, 253, 0.62);
            }}

            .info-value {{
                margin-top: 0.38rem;
                color: var(--ink-900);
                font-size: 1.02rem;
                font-weight: 800;
                line-height: 1.2;
            }}

            .dark .info-value {{
                color: #f8fbfd;
            }}

            .story-card {{
                margin-top: 0.95rem;
                padding: 1rem;
                border-radius: var(--radius-xl);
                background: rgba(255, 255, 255, 0.74);
                backdrop-filter: blur(14px);
                box-shadow: var(--shadow-soft);
                border: 1px solid rgba(255, 255, 255, 0.55);
            }}

            .story-card h3 {{
                margin: 0 0 0.6rem;
                font-family: Georgia, "Times New Roman", serif;
                font-size: 1.2rem;
                color: var(--ink-900);
            }}

            .story-card p {{
                margin: 0;
                color: var(--ink-700);
                line-height: 1.56;
                font-size: 0.95rem;
            }}

            .pill-list {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.48rem;
                margin-top: 0.85rem;
            }}

            .pill {{
                padding: 0.5rem 0.75rem;
                border-radius: 999px;
                background: rgba(14, 23, 38, 0.06);
                color: var(--ink-900);
                font-size: 0.78rem;
                font-weight: 700;
            }}

            .footer-note {{
                margin-top: 1rem;
                color: var(--ink-500);
                font-size: 0.8rem;
                line-height: 1.45;
                text-align: center;
            }}

            @media (max-width: 480px) {{
                .main .block-container {{
                    padding-top: 0.85rem;
                    padding-left: 0.85rem;
                    padding-right: 0.85rem;
                }}

                .bio-grid {{
                    grid-template-columns: 1fr 1fr;
                }}

                .hero-name {{
                    font-size: 1.8rem;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_top_shell(total_players: int, total_teams: int) -> None:
    st.markdown(
        f"""
        <section class="top-shell">
            <div class="eyebrow">{APP_TITLE}</div>
            <h1>{APP_SUBTITLE}</h1>
            <p>
                Visualizacao mobile pensada para navegar o elenco do Brasileirao de 2026
                com recorte por clube, posicao e atleta.
            </p>
            <p>
                {total_players} jogadores mapeados em {total_teams} times.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_filter_heading() -> None:
    st.markdown('<div class="section-title">Filtros</div>', unsafe_allow_html=True)


def render_player_hero(player: dict[str, Any]) -> None:
    age_value = f"{player['idade']} anos" if player["idade"] is not None else "Idade indisponivel"
    st.markdown(
        f"""
        <section class="hero-card" style="
            --team-primary: {player['team_primary']};
            --team-secondary: {player['team_secondary']};
            --team-text: {player['team_text']};
        ">
            <div class="hero-card-inner">
                <div class="hero-topline">
                    <div class="hero-tag">Pagina 1 - Bio</div>
                    <div class="team-badge">
                        <img src="{player['url_escudo_time']}" alt="Escudo do time">
                    </div>
                </div>
                <div class="player-photo-wrap">
                    <img src="{player['url_foto_jogador']}" alt="Foto do jogador">
                </div>
                <div>
                    <div class="hero-name">{player['nome_jogador']}</div>
                    <div class="hero-subline">
                        {player['team_name_display']} - {player['posicao_label']} - {age_value}
                    </div>
                    <div class="chip-row">
                        <div class="chip">Camisa #{player['shirt_number_display']}</div>
                        <div class="chip">{player['nacionalidade_display']}</div>
                        <div class="chip">{player['competicao_display']}</div>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_bio_grid(player: dict[str, Any]) -> None:
    info_items = [
        ("Time", player["team_name_display"], False),
        ("Sigla", player.get("sigla_time") or "--", False),
        ("Posicao Base", player.get("posicao_principal") or "--", False),
        ("Posicao Detalhada", player["posicao_label"], True),
        ("Nascimento", format_birth_date(player.get("data_nascimento")), False),
        ("Idade", f"{player['idade']} anos" if player["idade"] is not None else "--", False),
        ("Nacionalidade", player["nacionalidade_display"], False),
        ("Temporada", str(player.get("temporada") or "--"), False),
    ]

    st.markdown('<div class="section-title">Bio do Jogador</div>', unsafe_allow_html=True)

    cards = []
    for label, value, dark in info_items:
        dark_class = " dark" if dark else ""
        cards.append(
            f"""
            <div class="info-card{dark_class}">
                <div class="info-label">{label}</div>
                <div class="info-value">{value}</div>
            </div>
            """
        )

    st.markdown(f'<section class="bio-grid">{"".join(cards)}</section>', unsafe_allow_html=True)


def render_position_story(player: dict[str, Any]) -> None:
    alternative_positions = player["posicoes_alternativas"]
    if not alternative_positions:
        alternative_html = '<div class="pill">Sem variacoes mapeadas</div>'
    else:
        alternative_html = "".join(
            f'<div class="pill">{position}</div>' for position in alternative_positions
        )

    st.markdown(
        f"""
        <section class="story-card">
            <h3>Leitura rapida do perfil</h3>
            <p>
                {player['nome_jogador']} aparece na base do Brasileirao 2026 com papel principal de
                <strong> {player['posicao_label']}</strong>, defendendo o
                <strong> {player['team_name_display']}</strong>.
                Esta ficha prioriza os dados mais uteis para navegação inicial no elenco:
                identidade do atleta, recorte competitivo, idade esportiva e versatilidade posicional.
            </p>
            <div class="pill-list">
                {alternative_html}
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_footer(player: dict[str, Any]) -> None:
    st.markdown(
        f"""
        <div class="footer-note">
            Ultima captura registrada na base: {format_capture(player.get('capturado_em_utc'))}.
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_filters(players: list[dict[str, Any]]) -> dict[str, str | None]:
    team_options = sorted({player["team_name_display"] for player in players})

    selected_team = st.selectbox(
        "Time",
        options=["Todos os times", *team_options],
        index=0,
    )

    team_filtered_players = players
    if selected_team != "Todos os times":
        team_filtered_players = [
            player for player in team_filtered_players if player["team_name_display"] == selected_team
        ]

    position_options = sorted({player["posicao_label"] for player in team_filtered_players})
    selected_position = st.selectbox(
        "Posicao",
        options=["Todas as posicoes", *position_options],
        index=0,
    )

    filtered_players = team_filtered_players
    if selected_position != "Todas as posicoes":
        filtered_players = [player for player in filtered_players if player["posicao_label"] == selected_position]

    if not filtered_players:
        st.warning("Nenhum jogador encontrado para esse recorte.")
        st.stop()

    player_options = filtered_players
    player_labels = {
        player["id_jogador"]: f"{player['nome_jogador']} - {player['team_name_display']}"
        for player in player_options
    }

    selected_player_id = st.selectbox(
        "Jogador",
        options=[player["id_jogador"] for player in player_options],
        format_func=lambda player_id: player_labels[player_id],
        index=0,
    )

    return {
        "team": None if selected_team == "Todos os times" else selected_team,
        "position": None if selected_position == "Todas as posicoes" else selected_position,
        "player_id": selected_player_id,
    }


def main() -> None:
    st.set_page_config(
        page_title=f"{APP_TITLE} | Bio do Jogador",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    inject_styles()

    missing_settings = get_missing_database_settings()
    if missing_settings:
        st.error(
            "Configuracao de banco incompleta. Defina as credenciais em Streamlit Secrets "
            "ou nas variaveis de ambiente antes de publicar o app."
        )
        st.code("\n".join(missing_settings))
        return

    try:
        players = load_players()
    except Exception:
        st.error(
            "Nao foi possivel carregar os dados do banco neste momento. "
            "Revise os secrets do app e a conectividade com o banco."
        )
        return

    if not players:
        st.warning("Nenhum jogador disponivel para exibir.")
        return

    unique_teams = {player["team_name_display"] for player in players}
    render_top_shell(total_players=len(players), total_teams=len(unique_teams))
    render_filter_heading()
    filters = build_filters(players)

    selected_player = next(
        player for player in players if player["id_jogador"] == filters["player_id"]
    )

    render_player_hero(selected_player)
    render_bio_grid(selected_player)
    render_position_story(selected_player)
    render_footer(selected_player)


if __name__ == "__main__":
    main()
