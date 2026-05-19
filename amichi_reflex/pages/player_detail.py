from __future__ import annotations

from typing import Any

import reflex as rx

from ..components.shell import page_shell
from ..state import CatalogState
from ..theme import EDITORIAL_TITLE_STYLE, GLASS_PANEL_STYLE, SECTION_TITLE_STYLE, SOFT_PANEL_STYLE


PlayerRow = dict[str, Any]


def info_card(label: str, value: rx.Var | str, dark: bool = False) -> rx.Component:
    return rx.box(
        rx.text(
            label,
            font_size="0.72rem",
            font_weight="700",
            letter_spacing="0.12em",
            text_transform="uppercase",
            color="rgba(247,251,253,0.68)" if dark else "#73859b",
        ),
        rx.text(
            value,
            font_size="1rem",
            font_weight="700",
            color="#f7fbfd" if dark else "#0c1622",
            margin_top="0.4rem",
        ),
        padding="1rem",
        border_radius="22px",
        background="rgba(15,23,34,0.76)" if dark else "rgba(255,255,255,0.82)",
        border="1px solid rgba(255,255,255,0.12)" if dark else "1px solid rgba(12,22,34,0.08)",
        box_shadow="0 18px 42px rgba(15, 23, 34, 0.08)",
    )


def detail_hero(player: PlayerRow) -> rx.Component:
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.button(
                        "Voltar ao catalogo",
                        on_click=CatalogState.back_to_catalog,
                        radius="full",
                        variant="soft",
                        background="rgba(255,255,255,0.12)",
                        color="#f7fbfd",
                        class_name="amichi-ghost-button",
                    ),
                    rx.badge(
                        "Ficha premium",
                        radius="full",
                        variant="surface",
                        background="rgba(255,255,255,0.12)",
                        color="#f7fbfd",
                    ),
                    spacing="3",
                    wrap="wrap",
                ),
                rx.heading(
                    player["nome_jogador"],
                    size="9",
                    color="#f7fbfd",
                    **EDITORIAL_TITLE_STYLE,
                ),
                rx.text(
                    player["hero_summary"],
                    color="rgba(247, 251, 253, 0.84)",
                    font_size="1rem",
                    line_height="1.6",
                ),
                rx.flex(
                    rx.badge(
                        f"Camisa #{player['shirt_number_display']}",
                        radius="full",
                        variant="surface",
                        background="rgba(255,255,255,0.14)",
                        color="#f7fbfd",
                    ),
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
                    wrap="wrap",
                    gap="2",
                ),
                rx.box(
                    rx.text(
                        "Dossier visual",
                        font_size="0.72rem",
                        text_transform="uppercase",
                        letter_spacing="0.16em",
                        color="rgba(247,251,253,0.56)",
                    ),
                    rx.text(
                        "Composicao pensada para leitura rapida de identidade competitiva, funcao e contexto do atleta.",
                        color="rgba(247,251,253,0.84)",
                        line_height="1.55",
                        margin_top="0.5rem",
                        max_width="32rem",
                    ),
                    padding="1rem 1.05rem",
                    background="rgba(255,255,255,0.08)",
                    border="1px solid rgba(255,255,255,0.1)",
                    border_radius="24px",
                    width="100%",
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
                    height="18rem",
                    border_radius="28px",
                    background="rgba(255,255,255,0.16)",
                    border="1px solid rgba(255,255,255,0.18)",
                    padding="1rem",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    class_name="amichi-spotlight-photo",
                ),
                rx.image(
                    src=player["team_crest_display_url"],
                    alt="Escudo do clube",
                    width="4.2rem",
                    height="4.2rem",
                    object_fit="contain",
                    background="rgba(255,255,255,0.14)",
                    border_radius="22px",
                    padding="0.5rem",
                    border="1px solid rgba(255,255,255,0.14)",
                ),
                direction=rx.breakpoints(initial="column", md="row"),
                align="center",
                justify="center",
                gap="4",
                width="100%",
            ),
            direction=rx.breakpoints(initial="column", lg="row"),
            align="stretch",
            justify="between",
            gap="5",
            width="100%",
        ),
        padding=["1.35rem", "1.6rem", "2rem"],
        border_radius="34px",
        background=player["card_gradient"],
        box_shadow="0 30px 70px rgba(15, 23, 34, 0.18)",
        border="1px solid rgba(255,255,255,0.14)",
    )


def hero_metrics(player: PlayerRow) -> rx.Component:
    return rx.grid(
        info_card("Time", player["team_name_display"], dark=True),
        info_card("Posicao", player["posicao_label"]),
        info_card("Idade esportiva", player["idade_display"]),
        info_card("Nacionalidade", player["nacionalidade_display"]),
        columns=rx.breakpoints(initial="1", md="2", xl="4"),
        spacing="4",
        width="100%",
    )


def executive_sidebar(player: PlayerRow) -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.text("Executive Summary", **SECTION_TITLE_STYLE),
            rx.heading(
                player["versatility_label"],
                size="7",
                margin_top="0.35rem",
                **EDITORIAL_TITLE_STYLE,
            ),
            rx.text(
                player["executive_summary"],
                color="#415367",
                line_height="1.65",
                margin_top="0.7rem",
            ),
            rx.flex(
                rx.badge(
                    f"{player['alternative_positions_count']} variacoes",
                    radius="full",
                    variant="surface",
                    background="rgba(15,23,34,0.06)",
                ),
                rx.badge(
                    player["competicao_display"],
                    radius="full",
                    variant="outline",
                ),
                wrap="wrap",
                gap="2",
                margin_top="1rem",
            ),
            padding="1.2rem",
            width="100%",
            class_name="amichi-presentation-card",
            **SOFT_PANEL_STYLE,
        ),
        rx.box(
            rx.text("Leitura de banca", **SECTION_TITLE_STYLE),
            rx.text(
                "Esta tela foi desenhada para comunicar rapidamente hierarquia visual, contexto competitivo e clareza estrutural do projeto.",
                color="#233140",
                line_height="1.65",
                margin_top="0.55rem",
            ),
            rx.text(
                player["profile_note"],
                color="#6d7f92",
                line_height="1.6",
                margin_top="0.75rem",
            ),
            padding="1.2rem",
            width="100%",
            class_name="amichi-presentation-card",
            **GLASS_PANEL_STYLE,
        ),
        rx.box(
            rx.text("Ultima captura", **SECTION_TITLE_STYLE),
            rx.heading(
                player["captured_at_display"],
                size="5",
                margin_top="0.35rem",
                **EDITORIAL_TITLE_STYLE,
            ),
            rx.text(
                "Os dados permanecem vinculados ao Supabase, enquanto a camada visual foi redesenhada em Reflex para demonstracao e produto.",
                color="#415367",
                line_height="1.6",
                margin_top="0.7rem",
            ),
            padding="1.2rem",
            width="100%",
            class_name="amichi-presentation-card",
            **GLASS_PANEL_STYLE,
        ),
        spacing="4",
        width="100%",
        max_width="22rem",
    )


def detail_tabs(player: PlayerRow) -> rx.Component:
    return rx.tabs.root(
        rx.tabs.list(
            rx.tabs.trigger("Bio", value="bio"),
            rx.tabs.trigger("Posicoes", value="posicoes"),
            rx.tabs.trigger("Contexto", value="contexto"),
            size="2",
            width="fit-content",
            background="rgba(255,255,255,0.8)",
            border_radius="999px",
            padding="0.35rem",
            border="1px solid rgba(12,22,34,0.06)",
        ),
        rx.tabs.content(
            rx.grid(
                info_card("Time", player["team_name_display"]),
                info_card("Sigla", player["sigla_display"]),
                info_card("Posicao base", player["posicao_principal_display"]),
                info_card("Posicao detalhada", player["posicao_label"], dark=True),
                info_card("Nascimento", player["birth_date_display"]),
                info_card("Idade", player["idade_display"]),
                info_card("Nacionalidade", player["nacionalidade_display"]),
                info_card("Temporada", player["temporada_display"]),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="4",
                width="100%",
                margin_top="1rem",
            ),
            value="bio",
        ),
        rx.tabs.content(
            rx.box(
                rx.text("Leitura posicional", **SECTION_TITLE_STYLE),
                rx.heading(
                    player["posicao_label"],
                    size="7",
                    margin_top="0.35rem",
                    **EDITORIAL_TITLE_STYLE,
                ),
                rx.text(
                    "A ficha prioriza interpretacao rapida da funcao principal do atleta e exibe as alternativas mapeadas na base do projeto.",
                    color="#415367",
                    line_height="1.6",
                    margin_top="0.6rem",
                ),
                rx.flex(
                    rx.foreach(
                        CatalogState.selected_player_positions,
                        lambda position: rx.badge(
                            position,
                            radius="full",
                            variant="surface",
                            padding_x="0.85rem",
                            padding_y="0.5rem",
                        ),
                    ),
                    wrap="wrap",
                    gap="2",
                    margin_top="1rem",
                ),
                rx.text(
                    "As variacoes listadas ajudam a comunicar flexibilidade funcional e amplitude de uso dentro do elenco.",
                    color="#6d7f92",
                    line_height="1.6",
                    margin_top="1rem",
                ),
                margin_top="1rem",
                padding="1.15rem",
                **GLASS_PANEL_STYLE,
            ),
            value="posicoes",
        ),
        rx.tabs.content(
            rx.box(
                rx.grid(
                    info_card("Competicao", player["competicao_display"]),
                    info_card("Ultima captura", player["captured_at_display"]),
                    columns=rx.breakpoints(initial="1", md="2"),
                    spacing="4",
                    width="100%",
                ),
                rx.text(
                    "Os dados desta tela sao servidos a partir do Supabase e apresentados em uma camada editorial desenvolvida em Reflex.",
                    color="#415367",
                    line_height="1.6",
                    margin_top="1rem",
                ),
                rx.box(
                    rx.text(
                        "Nota de apresentacao",
                        font_size="0.72rem",
                        text_transform="uppercase",
                        letter_spacing="0.14em",
                        color="#7a8a9a",
                    ),
                    rx.text(
                        "A ficha prioriza clareza de leitura, hierarquia visual forte e uso com qualidade tanto em celular quanto em tela maior.",
                        color="#233140",
                        margin_top="0.45rem",
                        line_height="1.6",
                    ),
                    margin_top="1rem",
                    padding="0.95rem 1rem",
                    background="rgba(15,23,34,0.04)",
                    border="1px solid rgba(12,22,34,0.05)",
                    border_radius="20px",
                ),
                margin_top="1rem",
                padding="1.15rem",
                **GLASS_PANEL_STYLE,
            ),
            value="contexto",
        ),
        value=CatalogState.active_tab,
        on_change=CatalogState.set_active_tab,
        width="100%",
    )


def empty_selection() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("Nenhuma ficha ativa", **SECTION_TITLE_STYLE),
            rx.heading(
                "Selecione um atleta no catalogo para abrir a experiencia completa.",
                size="7",
                align="center",
                **EDITORIAL_TITLE_STYLE,
            ),
            rx.button(
                "Ir para o catalogo",
                on_click=CatalogState.back_to_catalog,
                radius="full",
                background="#0f1722",
                color="#f7fbfd",
            ),
            spacing="3",
            align="center",
        ),
        padding="2rem",
        **GLASS_PANEL_STYLE,
    )


def player_detail() -> rx.Component:
    player = CatalogState.selected_player
    return page_shell(
        rx.cond(
            CatalogState.has_selected_player,
            rx.vstack(
                detail_hero(player),
                hero_metrics(player),
                rx.flex(
                    rx.box(detail_tabs(player), width="100%", flex="1"),
                    executive_sidebar(player),
                    direction=rx.breakpoints(initial="column", xl="row"),
                    align="start",
                    gap="5",
                    width="100%",
                ),
                spacing="5",
                width="100%",
            ),
            empty_selection(),
        )
    )
