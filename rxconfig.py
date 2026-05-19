import reflex as rx

from amichi_reflex.theme import APP_THEME


config = rx.Config(
    app_name="amichi_reflex",
    plugins=[
        rx.plugins.RadixThemesPlugin(theme=APP_THEME),
        rx.plugins.SitemapPlugin(),
    ],
)
