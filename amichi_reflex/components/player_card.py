from __future__ import annotations

from typing import Any

import reflex as rx


PlayerRow = dict[str, Any]


def player_card(player: PlayerRow, open_action: rx.event.EventSpec) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.flex(
                rx.hstack(
                    rx.box(
                        background=player["card_gradient"],
                        width="0.55rem",
                        height="3.4rem",
                        border_radius="999px",
                        flex_shrink="0",
                    ),
                    rx.vstack(
                        rx.text(
                            player["team_name_display"],
                            font_size="0.75rem",
                            color="#73859b",
                            font_weight="600",
                            text_transform="uppercase",
                            letter_spacing="0.10em",
                        ),
                        rx.heading(
                            player["nome_jogador"],
                            size="5",
                            font_family="'Fraunces', serif",
                            color="#0c1622",
                            letter_spacing="-0.03em",
                        ),
                        rx.text(
                            player["posicao_label"],
                            font_size="0.98rem",
                            color="#344455",
                            weight="medium",
                        ),
                        spacing="1",
                        align="start",
                    ),
                    spacing="3",
                    align="start",
                    width="100%",
                ),
                rx.image(
                    src=player["team_crest_display_url"],
                    alt="Escudo do clube",
                    width="3rem",
                    height="3rem",
                    object_fit="contain",
                    border_radius="18px",
                    background="rgba(15, 23, 34, 0.04)",
                    padding="0.35rem",
                    flex_shrink="0",
                ),
                justify="between",
                align="start",
                width="100%",
                gap="3",
            ),
            rx.hstack(
                rx.badge(
                    "Perfil em destaque",
                    radius="full",
                    variant="surface",
                    size="1",
                    background="rgba(15, 23, 34, 0.05)",
                    color="#415367",
                ),
                rx.spacer(),
                rx.text(
                    player["team_name_display"],
                    font_size="0.8rem",
                    color="#7d8ea1",
                    font_weight="600",
                ),
                width="100%",
                align="center",
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
                    width=["100%", "11rem"],
                    min_width=["100%", "11rem"],
                    height="12rem",
                    border_radius="24px",
                    background="linear-gradient(180deg, rgba(222, 232, 240, 0.88), rgba(255, 255, 255, 0.96))",
                    border="1px solid rgba(12, 22, 34, 0.06)",
                    padding="0.8rem",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    overflow="hidden",
                ),
                rx.vstack(
                    rx.text(
                        player["hero_summary"],
                        color="#415367",
                        font_size="0.92rem",
                        line_height="1.5",
                    ),
                    rx.flex(
                        rx.badge(
                            f"Camisa #{player['shirt_number_display']}",
                            radius="full",
                            variant="soft",
                        ),
                        rx.badge(
                            player["nacionalidade_display"],
                            radius="full",
                            variant="surface",
                        ),
                        rx.badge(
                            player["competicao_display"],
                            radius="full",
                            variant="outline",
                        ),
                        wrap="wrap",
                        gap="2",
                    ),
                    rx.spacer(),
                    rx.button(
                        "Abrir ficha completa",
                        on_click=open_action,
                        radius="full",
                        size="3",
                        background="#0f1722",
                        color="#f7fbfd",
                        width=["100%", "fit-content"],
                        class_name="amichi-dark-button",
                    ),
                    align="start",
                    spacing="4",
                    width="100%",
                    height="100%",
                ),
                direction=rx.breakpoints(initial="column", md="row"),
                gap="4",
                width="100%",
                align="stretch",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        size="3",
        width="100%",
        border_radius="30px",
        background="rgba(255, 255, 255, 0.82)",
        border="1px solid rgba(12, 22, 34, 0.08)",
        box_shadow="0 26px 58px rgba(15, 23, 34, 0.08)",
        class_name="amichi-card-hover",
    )
