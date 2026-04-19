"""
Teste pentru Lab 5 — PySide6 GUI + SQLite + cozi de mesaje.

Testele acoperă doar logica pură (fără GUI):
- TextToHtmlConverter
- GameDatabase
"""

import sqlite3
import tempfile
import os
import pytest

from lab05.converter import TextToHtmlConverter
from lab05.game_db import GameDatabase


class TestTextToHtmlConverter:
    """Teste pentru conversia text → HTML."""

    def setup_method(self) -> None:
        """Creează o instanță nouă înainte de fiecare test."""
        self.converter = TextToHtmlConverter()

    def test_prima_linie_devine_h1(self) -> None:
        """Prima linie din text trebuie să apară ca <h1>."""
        text = "Titlul Meu\n\nUn paragraf."
        rezultat = self.converter.convert(text)
        assert "<h1>Titlul Meu</h1>" in rezultat

    def test_paragraf_devine_p(self) -> None:
        """Blocurile de text separate de linie goală devin <p>."""
        text = "Titlu\n\nPrimul paragraf.\n\nAl doilea paragraf."
        rezultat = self.converter.convert(text)
        assert "<p>Primul paragraf.</p>" in rezultat
        assert "<p>Al doilea paragraf.</p>" in rezultat

    def test_paragraf_simplu_fara_titlu_extra(self) -> None:
        """Prima linie e titlu, restul sunt paragrafe."""
        text = "Titlu\n\nConținut"
        rezultat = self.converter.convert(text)
        assert "<h1>Titlu</h1>" in rezultat
        assert "<p>Conținut</p>" in rezultat
        # Titlul nu apare și ca paragraf
        assert rezultat.count("<p>Titlu</p>") == 0

    def test_text_gol_returneaza_html_minimal(self) -> None:
        """Text gol trebuie să returneze un HTML valid (cel puțin taguri html/body)."""
        rezultat = self.converter.convert("")
        assert "<html>" in rezultat or "<!DOCTYPE" in rezultat or "<body>" in rezultat

    def test_un_singur_cuvant(self) -> None:
        """Un singur cuvânt devine titlu h1."""
        rezultat = self.converter.convert("Hello")
        assert "<h1>Hello</h1>" in rezultat

    def test_mai_multe_paragrafe(self) -> None:
        """Verifică că toate paragrafele sunt prezente."""
        text = "Titlu\n\nP1\n\nP2\n\nP3"
        rezultat = self.converter.convert(text)
        assert "<p>P1</p>" in rezultat
        assert "<p>P2</p>" in rezultat
        assert "<p>P3</p>" in rezultat

    def test_rezultat_este_string(self) -> None:
        """Metoda convert returnează întotdeauna un string."""
        assert isinstance(self.converter.convert("Test"), str)
        assert isinstance(self.converter.convert(""), str)

    def test_linii_consecutive_acelasi_paragraf(self) -> None:
        """Liniile consecutive (fără linie goală) fac parte din același paragraf."""
        text = "Titlu\n\nLinia 1\nLinia 2\nLinia 3"
        rezultat = self.converter.convert(text)
        # Toate cele 3 linii sunt în același bloc
        assert "<h1>Titlu</h1>" in rezultat
        # Paragraful conține cel puțin prima linie
        assert "Linia 1" in rezultat


class TestGameDatabase:
    """Teste pentru baza de date SQLite a jocului."""

    def setup_method(self) -> None:
        """Creează o bază de date temporară înainte de fiecare test."""
        self.tmp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp_file.close()
        self.db = GameDatabase(db_path=self.tmp_file.name)

    def teardown_method(self) -> None:
        """Curăță după fiecare test."""
        self.db.close()
        os.unlink(self.tmp_file.name)

    def test_insert_scor(self) -> None:
        """Inserarea unui scor nu aruncă eroare."""
        self.db.insert_score("Alice", 100)  # Nu trebuie să arunce excepție

    def test_get_scores_dupa_jucator(self) -> None:
        """Scorurile unui jucător sunt returnate corect."""
        self.db.insert_score("Alice", 100)
        self.db.insert_score("Alice", 200)
        self.db.insert_score("Bob", 50)

        scoruri_alice = self.db.get_scores("Alice")
        assert len(scoruri_alice) == 2

        scoruri_bob = self.db.get_scores("Bob")
        assert len(scoruri_bob) == 1

    def test_get_scores_jucator_inexistent(self) -> None:
        """Jucător fără scoruri returnează listă goală."""
        scoruri = self.db.get_scores("Inexistent")
        assert scoruri == []

    def test_scoruri_contin_numele_jucatorului(self) -> None:
        """Fiecare scor returnat conține numele jucătorului corect."""
        self.db.insert_score("Alice", 42)
        scoruri = self.db.get_scores("Alice")
        assert len(scoruri) > 0
        # Tuple: (id, player, score, timestamp) sau similar
        # Cel puțin un câmp conține "Alice"
        assert any("Alice" in str(camp) for camp in scoruri[0])

    def test_valoarea_scorului_este_corecta(self) -> None:
        """Valoarea inserată este recuperată corect."""
        self.db.insert_score("Bob", 999)
        scoruri = self.db.get_scores("Bob")
        assert any(999 == camp or "999" == str(camp) for camp in scoruri[0])

    def test_top_scores(self) -> None:
        """Top scoruri returnează rezultate sortate descrescător."""
        self.db.insert_score("Alice", 100)
        self.db.insert_score("Bob", 300)
        self.db.insert_score("Charlie", 200)

        top = self.db.get_top_scores(limit=3)
        assert len(top) == 3
        # Primul scor trebuie să fie cel mai mare
        scoruri_valori = [camp for t in top for camp in t if isinstance(camp, int) and camp > 10]
        if scoruri_valori:
            assert scoruri_valori[0] >= scoruri_valori[-1]

    def test_tabela_exista_in_db(self) -> None:
        """Verifică că tabela scores a fost creată în SQLite."""
        conn = sqlite3.connect(self.tmp_file.name)
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='scores'"
        )
        rezultat = cursor.fetchone()
        conn.close()
        assert rezultat is not None, "Tabela 'scores' nu există în baza de date"
