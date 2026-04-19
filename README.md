# Lab 5 — Python GUI (PySide6) + SQLite + Cozi de Mesaje

Template GitHub Classroom pentru laboratorul 5 de Programare Python.

## Conținut

- **`lab5/converter.py`** — Convertor text→HTML (stub de implementat)
- **`lab5/worker.py`** — Proces worker cu multiprocessing.Queue (stub)
- **`lab5/main_window.py`** — Fereastra principală PySide6 (stub)
- **`lab5/main.py`** — Entry point aplicație
- **`lab5/game_db.py`** — Bază de date SQLite pentru scor (bonus, stub)
- **`lab5/game.py`** — Logica jocului P2P (bonus, stub)
- **`tests/test_lab5.py`** — Suite de teste (nu modifica)

## Cum se rulează

```bash
# Rulare teste
uv run pytest

# Rulare teste cu output detaliat
uv run pytest -v

# Pornire aplicație (necesită display)
uv run python -m lab05.main
```

## Cum se instalează dependențele

```bash
uv sync
```

## Cerințe

- Python >= 3.11
- uv (package manager)
- PySide6 >= 6.8 (instalat automat cu `uv sync`)
