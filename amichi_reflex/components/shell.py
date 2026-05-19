from __future__ import annotations

import reflex as rx

from ..services.config import APP_TITLE
from ..theme import CONTENT_WIDTH_STYLE, GLASS_PANEL_STYLE, PAGE_SHELL_STYLE


def top_nav() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.hstack(
                rx.box(
                    width="2.8rem",
                    height="2.8rem",
                    border_radius="20px",
                    background="linear-gradient(155deg, #0f1722, #35526f)",
                    box_shadow="0 16px 36px rgba(15, 23, 34, 0.16)",
                    position="relative",
                    overflow="hidden",
                    flex_shrink="0",
                    _after={
                        "content": '""',
                        "position": "absolute",
                        "inset": "0.4rem",
                        "border": "1px solid rgba(255,255,255,0.16)",
                        "border_radius": "14px",
                    },
                ),
                rx.vstack(
                    rx.text(
                        APP_TITLE,
                        font_size="0.72rem",
                        font_weight="700",
                        letter_spacing="0.18em",
                        text_transform="uppercase",
                        color="#73859b",
                    ),
                    rx.heading(
                        "Sports Intelligence",
                        size="6",
                        font_family="'Fraunces', serif",
                        letter_spacing="-0.04em",
                        color="#0c1622",
                    ),
                    rx.text(
                        "Edition",
                        font_size="0.72rem",
                        color="#99a8b9",
                        letter_spacing="0.18em",
                        text_transform="uppercase",
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
            ),
            rx.spacer(),
            rx.hstack(
                rx.button(
                    "Catalogo",
                    variant="ghost",
                    radius="full",
                    on_click=rx.redirect("/"),
                    color="#0c1622",
                    class_name="amichi-nav-button",
                ),
                rx.button(
                    "Sobre",
                    variant="soft",
                    radius="full",
                    on_click=rx.redirect("/sobre"),
                    background="rgba(255,255,255,0.62)",
                    color="#0c1622",
                    class_name="amichi-nav-button",
                ),
                spacing="2",
            ),
            align="center",
            width="100%",
            padding="0.95rem 1.1rem",
            **GLASS_PANEL_STYLE,
        ),
        **CONTENT_WIDTH_STYLE,
    )


def page_shell(*children: rx.Component) -> rx.Component:
    return rx.box(
        rx.vstack(
            top_nav(),
            rx.box(*children, **CONTENT_WIDTH_STYLE),
            spacing="5",
            width="100%",
        ),
        **PAGE_SHELL_STYLE,
    )
