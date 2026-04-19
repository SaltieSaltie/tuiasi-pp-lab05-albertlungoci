"""
Logica jocului P2P (bonus).

Doi jucători comunică prin cozi System-V, iar scorurile
sunt stocate în SQLite prin GameDatabase.
"""

from lab05.game_db import GameDatabase


class Game:
    """Logica jocului P2P cu comunicare prin cozi System-V."""

    def __init__(self, player_name: str, db_path: str = "scores.db") -> None:
        """Inițializează jocul pentru un jucător.

        Args:
            player_name: Numele acestui jucător.
            db_path: Calea către baza de date SQLite.
        """
        # TODO: Salvează player_name
        # TODO: Creează instanță GameDatabase
        # TODO: Inițializează cozile System-V (sysv_ipc sau alternativă)
        raise NotImplementedError("De implementat")

    def send_move(self, move: str) -> None:
        """Trimite o mutare celuilalt jucător prin coada System-V.

        Args:
            move: Mutarea de trimis (ex: "rock", "paper", "scissors").
        """
        # TODO: Trimite mutarea prin coada System-V
        raise NotImplementedError("De implementat")

    def receive_move(self) -> str:
        """Primește mutarea celuilalt jucător.

        Returns:
            Mutarea primită ca string.
        """
        # TODO: Citește din coada System-V
        raise NotImplementedError("De implementat")

    def play_round(self, my_move: str) -> str:
        """Joacă o rundă: trimite mutarea și determină câștigătorul.

        Args:
            my_move: Mutarea acestui jucător.

        Returns:
            "win", "lose" sau "draw".
        """
        # TODO: Trimite mutarea, primește mutarea adversarului
        # TODO: Determină rezultatul și salvează scorul
        raise NotImplementedError("De implementat")

    def close(self) -> None:
        """Curăță resursele (cozi, conexiune DB)."""
        # TODO: Eliberează cozile System-V și închide DB
        raise NotImplementedError("De implementat")
