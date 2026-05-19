from __future__ import annotations

from typing import Any

import reflex as rx

from ..components.player_card import player_card
from ..components.shell import page_shell
from ..services.config import APP_SUBTITLE
from ..state import CatalogState
from ..theme import (
    DARK_PANEL_STYLE,
    EDITORIAL_TITLE_STYLE,
    GLASS_PANEL_STYLE,
    SECTION_TITLE_STYLE,
    SOFT_PANEL_STYLE,
)


PlayerRow = dict[str, Any]


def _summary_card(label: str, value: rx.Var | int, body: str) -> rx.Component:
    return rx.box(
        rx.text(
            label,
            font_size="0.75rem",
            font_weight="700",
            letter_spacing="0.14em",
            text_transform="uppercase",
            color="rgba(247, 251, 253, 0.66)",
        ),
        rx.heading(
            value,
            size="8",
            font_family="'Fraunces', serif",
            letter_spacing="-0.04em",
            color="#f7fbfd",
        ),
        rx.text(
            body,
            color="rgba(247, 251, 253, 0.74)",
            font_size="0.88rem",
            line_height="1.5",
        ),
        background="rgba(255,255,255,0.08)",
        border="1px solid rgba(255,255,255,0.12)",
        border_radius="24px",
        padding="1rem",
        width="100%",
    )


def hero_banner() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.badge(
                        "Amichi Score",
                        radius="full",
                        variant="soft",
                        size="2",
                        background="rgba(255,255,255,0.12)",
                        color="#f7fbfd",
                    ),
                    rx.badge(
                        "Visual Edition",
                        radius="full",
                        variant="surface",
                        size="2",
                        background="rgba(255,255,255,0.08)",
                        color="rgba(247,251,253,0.86)",
                    ),
                    spacing="2",
                    wrap="wrap",
                ),
                rx.heading(
                    APP_SUBTITLE,
                    size="9",
                    color="#f7fbfd",
                    **EDITORIAL_TITLE_STYLE,
                ),
                rx.text(
                    "Leitura visual de jogadores, elencos e versatilidade posicional "
                    "com acabamento mobile-first e linguagem de plataforma profissional.",
                    color="rgba(247, 251, 253, 0.82)",
                    font_size=["0.98rem", "1.02rem", "1.08rem"],
                    max_width="36rem",
                    line_height="1.65",
                ),
                rx.grid(
                    rx.box(
                        rx.text(
                            "Direcao",
                            font_size="0.72rem",
                            letter_spacing="0.16em",
                            text_transform="uppercase",
                            color="rgba(247,251,253,0.56)",
                        ),
                        rx.text(
                            "Scouting, contexto competitivo e leitura editorial de atletas.",
                            color="#f7fbfd",
                            margin_top="0.4rem",
                            line_height="1.55",
                        ),
                        padding="0.95rem 1rem",
                        background="rgba(255,255,255,0.08)",
                        border="1px solid rgba(255,255,255,0.1)",
                        border_radius="22px",
                    ),
                    rx.box(
                        rx.text(
                            "Experiencia",
                            font_size="0.72rem",
                            letter_spacing="0.16em",
                            text_transform="uppercase",
                            color="rgba(247,251,253,0.56)",
                        ),
                        rx.text(
                            "Catalogo navegavel, atleta em foco e ficha detalhada de apresentacao.",
                            color="#f7fbfd",
                            margin_top="0.4rem",
                            line_height="1.55",
                        ),
                        padding="0.95rem 1rem",
                        background="rgba(255,255,255,0.08)",
                        border="1px solid rgba(255,255,255,0.1)",
                        border_radius="22px",
                    ),
                    columns=rx.breakpoints(initial="1", md="2"),
                    spacing="3",
                    width="100%",
                ),
                rx.hstack(
                    rx.button(
                        "Explorar atletas",
                        radius="full",
                        size="3",
                        background="#f7fbfd",
                        color="#0f1722",
                        on_click=rx.scroll_to("player-grid"),
                        class_name="amichi-light-button",
                    ),
                    rx.button(
                        "Ver conceito",
                        radius="full",
                        size="3",
                        variant="outline",
                        color="#f7fbfd",
                        border_color="rgba(255,255,255,0.34)",
                        on_click=rx.redirect("/sobre"),
                        class_name="amichi-ghost-button",
                    ),
                    spacing="3",
                    wrap="wrap",
                ),
                spacing="4",
                align="start",
                width="100%",
            ),
            rx.vstack(
                rx.grid(
                    _summary_card(
                        "Jogadores mapeados",
                        CatalogState.total_players,
                        "Base viva para leitura de elenco e perfil competitivo.",
                    ),
                    _summary_card(
                        "Clubes ativos",
                        CatalogState.total_teams,
                        "Cobertura organizada para navegacao e comparacao visual.",
                    ),
                    columns=rx.breakpoints(initial="1", lg="2"),
                    spacing="4",
                    width="100%",
                ),
                rx.box(
                    rx.text(
                        "Projeto academico com ambicao de produto.",
                        color="rgba(247,251,253,0.86)",
                        font_weight="600",
                        line_height="1.6",
                    ),
                    rx.text(
                        "A interface foi redesenhada em Reflex para apresentar dados esportivos com uma narrativa visual mais forte, clara e profissional.",
                        color="rgba(247,251,253,0.66)",
                        margin_top="0.45rem",
                        line_height="1.6",
                    ),
                    padding="1.1rem 1.2rem",
                    background="rgba(255,255,255,0.08)",
                    border="1px solid rgba(255,255,255,0.1)",
                    border_radius="24px",
                    width="100%",
                ),
                spacing="4",
                width="100%",
                max_width="31rem",
            ),
            direction=rx.breakpoints(initial="column", lg="row"),
            align="stretch",
            justify="between",
            gap="5",
            width="100%",
        ),
        padding=["1.35rem", "1.8rem", "2.15rem"],
        position="relative",
        overflow="hidden",
        class_name="amichi-hero-card",
        **DARK_PANEL_STYLE,
    )


def filter_panel() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.text("Painel de exploracao", **SECTION_TITLE_STYLE),
                rx.heading(
                    "Refine o elenco com criterio de scouting.",
                    size="7",
                    **EDITORIAL_TITLE_STYLE,
                ),
                rx.text(
                    "Busque por atleta, recorte por clube e afine a leitura por funcao tatico-posicional.",
                    color="#415367",
                    line_height="1.6",
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            rx.flex(
                rx.input(
                    placeholder="Buscar nome, clube, nacionalidade ou posicao",
                    value=CatalogState.search_term,
                    on_change=CatalogState.set_search_term,
                    size="3",
                    radius="large",
                    width="100%",
                    background="rgba(255,255,255,0.92)",
                ),
                rx.select(
                    items=CatalogState.team_options,
                    value=CatalogState.selected_team,
                    on_change=CatalogState.set_selected_team,
                    size="3",
                    radius="large",
                    width="100%",
                    variant="surface",
                ),
                rx.select(
                    items=CatalogState.position_options,
                    value=CatalogState.selected_position,
                    on_change=CatalogState.set_selected_position,
                    size="3",
                    radius="large",
                    width="100%",
                    variant="surface",
                ),
                rx.button(
                    "Limpar filtros",
                    on_click=CatalogState.reset_filters,
                    radius="full",
                    size="3",
                    background="#0f1722",
                    color="#f7fbfd",
                    width=["100%", "100%", "fit-content"],
                    class_name="amichi-dark-button",
                ),
                direction=rx.breakpoints(initial="column", lg="row"),
                align="stretch",
                gap="3",
                width="100%",
            ),
            direction=rx.breakpoints(initial="column", lg="row"),
            justify="between",
            align="stretch",
            gap="5",
            width="100%",
        ),
        padding=["1.15rem", "1.35rem", "1.6rem"],
        class_name="amichi-filter-panel",
        **GLASS_PANEL_STYLE,
    )


def active_filters_row() -> rx.Component:
    return rx.cond(
        CatalogState.has_active_filters,
        rx.box(
            rx.hstack(
                rx.text("Filtros ativos", **SECTION_TITLE_STYLE),
                rx.badge(
                    CatalogState.visible_count,
                    radius="full",
                    variant="surface",
                    background="rgba(15,23,34,0.06)",
                    color="#0c1622",
                ),
                spacing="3",
                wrap="wrap",
            ),
            rx.flex(
                rx.foreach(
                    CatalogState.active_filter_labels,
                    lambda label: rx.badge(
                        label,
                        radius="full",
                        variant="surface",
                        padding_x="0.9rem",
                        padding_y="0.55rem",
                        background="rgba(255,255,255,0.9)",
                        color="#233140",
                    ),
                ),
                wrap="wrap",
                gap="2",
                margin_top="0.9rem",
            ),
            padding="1rem 1.1rem",
            **SOFT_PANEL_STYLE,
        ),
        rx.fragment(),
    )


def spotlight_panel(player: PlayerRow) -> rx.Component:
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.text(
                    "Atleta em foco",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.14em",
                    text_transform="uppercase",
                    color="rgba(247,251,253,0.68)",
                ),
                rx.heading(
                    player["nome_jogador"],
                    size="8",
                    color="#f7fbfd",
                    **EDITORIAL_TITLE_STYLE,
                ),
                rx.text(
                    player["hero_summary"],
                    color="rgba(247,251,253,0.84)",
                    line_height="1.6",
                    font_size="1rem",
                    max_width="34rem",
                ),
                rx.flex(
                    rx.badge(
                        player["competicao_display"],
                        radius="full",
                        variant="surface",
                        background="rgba(255,255,255,0.14)",
                        color="#f7fbfd",
                    ),
                    rx.badge(
                        player["nacionalidade_display"],
                        radius="full",
                        variant="surface",
                        background="rgba(255,255,255,0.14)",
                        color="#f7fbfd",
                    ),
                    rx.badge(
                        f"Camisa #{player['shirt_number_display']}",
                        radius="full",
                        variant="surface",
                        background="rgba(255,255,255,0.14)",
                        color="#f7fbfd",
                    ),
                    wrap="wrap",
                    gap="2",
                ),
                rx.button(
                    "Abrir ficha premium",
                    on_click=CatalogState.open_player(player["id_jogador"]),
                    radius="full",
                    background="#f7fbfd",
                    color="#0f1722",
                    class_name="amichi-light-button",
                ),
                spacing="4",
                align="start",
                width="100%",
            ),
            rx.flex(
                rx.box(
                    rx.image(
                        src=player["player_photo_display_url"],
                        alt=f"Foto de {player['nome_jogador']}",
                        width="100%",
                        height="100%",
                        object_fit="contain",
                    ),
                    width=["100%", "18rem"],
                    height=["14rem", "17rem"],
                    padding="1rem",
                    border_radius="30px",
                    background="rgba(255,255,255,0.14)",
                    border="1px solid rgba(255,255,255,0.18)",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    class_name="amichi-spotlight-photo",
                ),
                rx.vstack(
                    rx.image(
                        src=player["team_crest_display_url"],
                        alt="Escudo do clube",
                        width="4rem",
                        height="4rem",
                        object_fit="contain",
                        border_radius="22px",
                        background="rgba(255,255,255,0.14)",
                        padding="0.5rem",
                    ),
                    rx.box(
                        rx.text(
                            "Leitura editorial",
                            font_size="0.72rem",
                            text_transform="uppercase",
                            letter_spacing="0.16em",
                            color="rgba(247,251,253,0.56)",
                        ),
                        rx.text(
                            "Painel criado para destacar rapidamente identidade competitiva, papel tatico e contexto do atleta.",
                            color="rgba(247,251,253,0.84)",
                            line_height="1.55",
                            margin_top="0.5rem",
                            max_width="16rem",
                        ),
                        padding="1rem",
                        background="rgba(255,255,255,0.08)",
                        border="1px solid rgba(255,255,255,0.1)",
                        border_radius="24px",
                        width="100%",
                    ),
                    spacing="3",
                    align="start",
                    width="100%",
                    max_width="18rem",
                ),
                direction=rx.breakpoints(initial="column", md="row"),
                align="center",
                justify="center",
                gap="4",
                width="100%",
            ),
            direction=rx.breakpoints(initial="column", lg="row"),
            justify="between",
            align="stretch",
            gap="5",
            width="100%",
        ),
        padding=["1.2rem", "1.5rem", "1.8rem"],
        background=player["card_gradient"],
        border="1px solid rgba(255,255,255,0.16)",
        border_radius="32px",
        box_shadow="0 30px 72px rgba(15, 23, 34, 0.14)",
        position="relative",
        overflow="hidden",
        class_name="amichi-spotlight-card",
    )


def loading_grid() -> rx.Component:
    return rx.grid(
        *[
            rx.box(
                height="20rem",
                border_radius="28px",
                background="linear-gradient(180deg, rgba(255,255,255,0.86), rgba(232,238,242,0.86))",
                border="1px solid rgba(12, 22, 34, 0.05)",
                box_shadow="0 20px 50px rgba(15, 23, 34, 0.06)",
            )
            for _ in range(3)
        ],
        columns="1",
        spacing="4",
        width="100%",
    )


def empty_state() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("Resultado vazio", **SECTION_TITLE_STYLE),
            rx.heading(
                "Nenhum atleta encontrado para esse recorte.",
                size="6",
                align="center",
                **EDITORIAL_TITLE_STYLE,
            ),
            rx.text(
                "Experimente limpar os filtros ou abrir mais clubes e posicoes para recuperar o universo completo.",
                color="#415367",
                align="center",
                max_width="34rem",
            ),
            rx.button(
                "Resetar filtros",
                on_click=CatalogState.reset_filters,
                radius="full",
                background="#0f1722",
                color="#f7fbfd",
                class_name="amichi-dark-button",
            ),
            spacing="3",
            align="center",
        ),
        padding="2rem",
        **GLASS_PANEL_STYLE,
    )


def results_header() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.text("Elenco navegavel", **SECTION_TITLE_STYLE),
            rx.heading(
                "Catalogo de atletas",
                size="7",
                **EDITORIAL_TITLE_STYLE,
            ),
            rx.text(
                "Cada ficha foi desenhada para leitura rapida, comparacao e impacto visual em apresentacao.",
                color="#415367",
            ),
            spacing="1",
            align="start",
        ),
        rx.vstack(
            rx.badge(
                CatalogState.visible_count,
                radius="full",
                variant="surface",
                size="2",
                padding_x="0.9rem",
                padding_y="0.55rem",
                font_size="0.88rem",
            ),
            rx.text(
                "Atletas visiveis no recorte atual",
                font_size="0.78rem",
                color="#8493a4",
            ),
            spacing="1",
            align=rx.breakpoints(initial="start", md="end"),
        ),
        direction=rx.breakpoints(initial="column", md="row"),
        align=rx.breakpoints(initial="start", md="center"),
        justify="between",
        gap="3",
        width="100%",
    )


def render_player(player: PlayerRow) -> rx.Component:
    return player_card(player, CatalogState.open_player(player["id_jogador"]))


def catalog_grid() -> rx.Component:
    return rx.box(
        results_header(),
        rx.cond(
            CatalogState.visible_count > 0,
            rx.grid(
                rx.foreach(CatalogState.visible_players, render_player),
                id="player-grid",
                columns=rx.breakpoints(initial="1", xl="2"),
                spacing="4",
                width="100%",
                margin_top="1rem",
            ),
            rx.box(empty_state(), margin_top="1rem"),
        ),
        width="100%",
    )


def error_banner() -> rx.Component:
    return rx.box(
        rx.text("Falha de carregamento", **SECTION_TITLE_STYLE),
        rx.heading(
            "Nao foi possivel montar o catalogo agora.",
            size="6",
            **EDITORIAL_TITLE_STYLE,
        ),
        rx.text(CatalogState.error_message, color="#7b2531", line_height="1.6"),
        padding="1.25rem",
        border_radius="26px",
        background="rgba(255, 240, 242, 0.9)",
        border="1px solid rgba(168, 52, 76, 0.16)",
    )


def index() -> rx.Component:
    return page_shell(
        hero_banner(),
        filter_panel(),
        active_filters_row(),
        rx.cond(
            CatalogState.has_selected_player,
            spotlight_panel(CatalogState.selected_player),
            rx.fragment(),
        ),
        rx.cond(
            CatalogState.error_message != "",
            error_banner(),
            rx.cond(CatalogState.is_loading, loading_grid(), catalog_grid()),
        ),
    )
