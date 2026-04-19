"""
Baza de date SQLite pentru jocul P2P (bonus).

Stochează scorurile jucătorilor în fișierul scores.db.
"""

import sqlite3
from pathlib import Path


class GameDatabase:
    """CRUD simplu pentru scorurile jocului P2P."""

    def __init__(self, db_path: str = "scores.db") -> None:
        """Inițializează conexiunea la baza de date și creează tabela dacă lipsește.

        Args:
            db_path: Calea către fișierul SQLite.
        """
        # TODO: Deschide conexiunea sqlite3
        # TODO: Creează tabela scores(id, player, score, timestamp) dacă nu există
        raise NotImplementedError("De implementat")

    def insert_score(self, player: str, score: int) -> None:
        """Inserează un scor nou pentru un jucător.

        Args:
            player: Numele jucătorului.
            score: Scorul obținut.
        """
        # TODO: Inserează un rând în tabela scores cu timestamp curent
        raise NotImplementedError("De implementat")

    def get_scores(self, player: str) -> list[tuple[int, str, int, str]]:
        """Returnează toate scorurile unui jucător.

        Args:
            player: Numele jucătorului.

        Returns:
            Listă de tuple (id, player, score, timestamp).
        """
        # TODO: SELECT din scores WHERE player = ?
        raise NotImplementedError("De implementat")

    def get_top_scores(self, limit: int = 10) -> list[tuple[int, str, int, str]]:
        """Returnează cele mai mari scoruri din baza de date.

        Args:
            limit: Numărul maxim de rezultate.

        Returns:
            Listă de tuple (id, player, score, timestamp) sortate descrescător.
        """
        # TODO: SELECT top scoruri
        raise NotImplementedError("De implementat")

    def close(self) -> None:
        """Închide conexiunea la baza de date."""
        # TODO: Închide conexiunea
        raise NotImplementedError("De implementat")
