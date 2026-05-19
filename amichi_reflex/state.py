from __future__ import annotations

from typing import Any

import reflex as rx

from .services.config import get_missing_supabase_settings
from .services.players import (
    build_position_options,
    build_team_options,
    filter_players,
    load_players,
)


PlayerRow = dict[str, Any]


class CatalogState(rx.State):
    players: list[PlayerRow] = []
    visible_players: list[PlayerRow] = []
    team_options: list[str] = ["Todos os times"]
    position_options: list[str] = ["Todas as posicoes"]
    selected_team: str = "Todos os times"
    selected_position: str = "Todas as posicoes"
    selected_player_id: str = ""
    search_term: str = ""
    active_tab: str = "bio"
    is_loading: bool = False
    error_message: str = ""

    def _players_for_selected_team(self) -> list[PlayerRow]:
        if self.selected_team == "Todos os times":
            return self.players
        return [player for player in self.players if player["team_name_display"] == self.selected_team]

    def _recompute_position_options(self) -> None:
        team_scoped_players = self._players_for_selected_team()
        self.position_options = build_position_options(team_scoped_players)
        if self.selected_position not in self.position_options:
            self.selected_position = "Todas as posicoes"

    def _apply_filters(self) -> None:
        self.visible_players = filter_players(
            players=self.players,
            selected_team=self.selected_team,
            selected_position=self.selected_position,
            search_term=self.search_term,
        )
        if self.visible_players and self.selected_player_id not in {
            str(player["id_jogador"]) for player in self.visible_players
        }:
            self.selected_player_id = str(self.visible_players[0]["id_jogador"])

    @rx.event
    def load_catalog(self) -> None:
        if self.players or self.is_loading:
            return

        missing = get_missing_supabase_settings()
        if missing:
            self.error_message = (
                "Configuracao do Supabase incompleta. Defina: " + ", ".join(missing)
            )
            return

        self.is_loading = True
        try:
            players = load_players()
            self.players = players
            self.team_options = build_team_options(players)
            self._recompute_position_options()
            self._apply_filters()
            self.error_message = ""
            if players and not self.selected_player_id:
                self.selected_player_id = str(players[0]["id_jogador"])
        except Exception as exc:
            self.error_message = (
                "Nao foi possivel carregar o catalogo do Supabase no momento. "
                f"Detalhe: {exc}"
            )
        finally:
            self.is_loading = False

    @rx.event
    def set_search_term(self, value: str) -> None:
        self.search_term = value
        self._apply_filters()

    @rx.event
    def set_selected_team(self, value: str) -> None:
        self.selected_team = value or "Todos os times"
        self._recompute_position_options()
        self._apply_filters()

    @rx.event
    def set_selected_position(self, value: str) -> None:
        self.selected_position = value or "Todas as posicoes"
        self._apply_filters()

    @rx.event
    def reset_filters(self) -> None:
        self.selected_team = "Todos os times"
        self.selected_position = "Todas as posicoes"
        self.search_term = ""
        self._recompute_position_options()
        self._apply_filters()

    @rx.event
    def open_player(self, player_id: str) -> rx.event.EventSpec:
        self.selected_player_id = str(player_id)
        self.active_tab = "bio"
        return rx.redirect("/jogador")

    @rx.event
    def back_to_catalog(self) -> rx.event.EventSpec:
        return rx.redirect("/")

    @rx.event
    def set_active_tab(self, value: str) -> None:
        self.active_tab = value

    @rx.var
    def total_players(self) -> int:
        return len(self.players)

    @rx.var
    def total_teams(self) -> int:
        return max(len(self.team_options) - 1, 0)

    @rx.var
    def visible_count(self) -> int:
        return len(self.visible_players)

    @rx.var
    def has_active_filters(self) -> bool:
        return any(
            [
                self.selected_team != "Todos os times",
                self.selected_position != "Todas as posicoes",
                bool(self.search_term.strip()),
            ]
        )

    @rx.var
    def active_filter_labels(self) -> list[str]:
        labels: list[str] = []
        if self.selected_team != "Todos os times":
            labels.append(f"Clube: {self.selected_team}")
        if self.selected_position != "Todas as posicoes":
            labels.append(f"Posicao: {self.selected_position}")
        if self.search_term.strip():
            labels.append(f"Busca: {self.search_term.strip()}")
        return labels

    @rx.var
    def selected_player(self) -> PlayerRow:
        for player in self.players:
            if str(player["id_jogador"]) == self.selected_player_id:
                return player
        return self.players[0] if self.players else {}

    @rx.var
    def has_selected_player(self) -> bool:
        return bool(self.selected_player)

    @rx.var
    def selected_player_positions(self) -> list[str]:
        player = self.selected_player
        positions = player.get("posicoes_alternativas", [])
        if isinstance(positions, list):
            return [str(position) for position in positions]
        return []
