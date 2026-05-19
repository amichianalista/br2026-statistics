from __future__ import annotations

import reflex as rx

from ..components.shell import page_shell
from ..theme import EDITORIAL_TITLE_STYLE, GLASS_PANEL_STYLE, SECTION_TITLE_STYLE


def _about_card(label: str, title: str, body: str) -> rx.Component:
    return rx.box(
        rx.text(label, **SECTION_TITLE_STYLE),
        rx.heading(title, size="6", margin_top="0.35rem", **EDITORIAL_TITLE_STYLE),
        rx.text(body, color="#415367", line_height="1.7", margin_top="0.7rem"),
        padding="1.2rem",
        **GLASS_PANEL_STYLE,
    )


def about() -> rx.Component:
    return page_shell(
        rx.box(
            rx.text("Sobre o projeto", **SECTION_TITLE_STYLE),
            rx.heading(
                "Um app academico com acabamento de produto digital.",
                size="9",
                margin_top="0.35rem",
                **EDITORIAL_TITLE_STYLE,
            ),
            rx.text(
                "Esta versao em Reflex foi pensada para apresentar elenco, contexto competitivo e leitura posicional com impacto visual, clareza e responsividade real.",
                color="#415367",
                line_height="1.7",
                margin_top="0.9rem",
                max_width="46rem",
            ),
            padding="1.4rem 0 0.25rem",
        ),
        rx.grid(
            _about_card(
                "Dados",
                "Supabase como camada de base",
                "O catalogo de jogadores e clubes continua alimentado por consultas Python ao Supabase, preservando a logica do projeto original.",
            ),
            _about_card(
                "Interface",
                "Reflex para produto e apresentacao",
                "A camada visual foi redesenhada para mobile-first, com hierarquia editorial, glass surfaces, hero premium e paginas com navegacao mais madura.",
            ),
            _about_card(
                "Objetivo",
                "Impacto academico e clareza de leitura",
                "A proposta e mostrar dominio de dados, design de interface e organizacao de arquitetura em um unico trabalho coerente.",
            ),
            columns=rx.breakpoints(initial="1", lg="3"),
            spacing="4",
            width="100%",
        ),
    )
