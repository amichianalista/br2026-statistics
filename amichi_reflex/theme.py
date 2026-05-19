from __future__ import annotations

import reflex as rx

from .services.config import asset_url


FONT_STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Sora:wght@400;500;600;700&display=swap",
    asset_url("reflex.css"),
]

APP_THEME = rx.theme(
    appearance="light",
    has_background=True,
    accent_color="gray",
    gray_color="slate",
)

APP_STYLE = {
    "font_family": "'Sora', sans-serif",
    "background": "linear-gradient(180deg, #f3f6f8 0%, #ebf0f4 100%)",
    "color": "#0c1622",
}

PAGE_SHELL_STYLE = {
    "width": "100%",
    "min_height": "100vh",
    "padding_x": ["1rem", "1.25rem", "1.5rem"],
    "padding_y": ["1rem", "1.25rem", "1.75rem"],
}

CONTENT_WIDTH_STYLE = {
    "width": "100%",
    "max_width": "74rem",
    "margin_x": "auto",
}

GLASS_PANEL_STYLE = {
    "background": "rgba(255, 255, 255, 0.78)",
    "border": "1px solid rgba(12, 22, 34, 0.08)",
    "backdrop_filter": "blur(18px)",
    "box_shadow": "0 24px 60px rgba(15, 23, 34, 0.08)",
    "border_radius": "28px",
}

DARK_PANEL_STYLE = {
    "background": "linear-gradient(155deg, rgba(11, 20, 31, 0.96), rgba(28, 51, 80, 0.88))",
    "border": "1px solid rgba(255, 255, 255, 0.12)",
    "box_shadow": "0 30px 72px rgba(15, 23, 34, 0.18)",
    "border_radius": "32px",
}

SOFT_PANEL_STYLE = {
    "background": "linear-gradient(180deg, rgba(255,255,255,0.94), rgba(247,250,252,0.86))",
    "border": "1px solid rgba(12, 22, 34, 0.06)",
    "box_shadow": "0 18px 48px rgba(15, 23, 34, 0.06)",
    "border_radius": "26px",
}

SECTION_TITLE_STYLE = {
    "font_size": "0.75rem",
    "font_weight": "700",
    "letter_spacing": "0.14em",
    "text_transform": "uppercase",
    "color": "#718399",
}

EDITORIAL_TITLE_STYLE = {
    "font_family": "'Fraunces', serif",
    "letter_spacing": "-0.04em",
    "line_height": "0.98",
}
