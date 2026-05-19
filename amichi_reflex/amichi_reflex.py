from __future__ import annotations

import reflex as rx

from .pages.about import about
from .pages.home import index
from .pages.player_detail import player_detail
from .state import CatalogState
from .theme import APP_STYLE, FONT_STYLESHEETS


app = rx.App(
    style=APP_STYLE,
    stylesheets=FONT_STYLESHEETS,
    html_lang="pt-BR",
)

app.add_page(
    index,
    route="/",
    title="Amichi Score | Brasileirao 2026",
    description="Catalogo premium de atletas do Brasileirao 2026.",
    on_load=CatalogState.load_catalog,
)

app.add_page(
    player_detail,
    route="/jogador",
    title="Amichi Score | Ficha do Jogador",
    description="Ficha premium do atleta selecionado.",
    on_load=CatalogState.load_catalog,
)

app.add_page(
    about,
    route="/sobre",
    title="Amichi Score | Sobre o Projeto",
    description="Contexto do projeto e arquitetura da refatoracao visual em Reflex.",
)
