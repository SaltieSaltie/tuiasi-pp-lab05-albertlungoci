# Lab 5 — Python GUI (PySide6) + SQLite + Cozi de Mesaje

## Descriere

În acest laborator vei construi o aplicație desktop cu interfață grafică PySide6 care procesează fișiere text folosind comunicare inter-proces prin `multiprocessing.Queue`. Ca bonus, vei implementa un joc P2P cu comunicare prin cozi System-V și stocare a scorurilor în SQLite.

## Structura proiectului

```
lab05/
  lab5/
    __init__.py
    converter.py      ← logica de conversie text→HTML (stub)
    worker.py         ← proces worker cu cozi (stub)
    main_window.py    ← fereastra PySide6 (stub)
    main.py           ← entry point
    game_db.py        ← baza de date SQLite pentru joc (bonus, stub)
    game.py           ← logica jocului P2P (bonus, stub)
  tests/
    __init__.py
    test_lab5.py      ← teste complete
  .github/workflows/classroom.yml
  pyproject.toml
  ASSIGNMENT.md
  README.md
```

## Cerințe

### Tema 1 — Convertor text→HTML cu coadă de mesaje (obligatorie)

#### 1.1 `converter.py` — Clasa `TextToHtmlConverter`

Implementează metoda `convert(text: str) -> str`:

- **Prima linie** din text devine `<h1>Titlu</h1>`
- **Blocurile** separate de linie goală devin `<p>paragraf</p>`
- **Text gol** returnează un document HTML minimal valid (ex: `<html><body></body></html>`)
- Rezultatul trebuie să fie un document HTML complet (cu `<html>`, `<head>`, `<body>`)

**Exemplu:**
```python
converter = TextToHtmlConverter()
text = """Titlul Documentului

Primul paragraf cu mai
multe linii.

Al doilea paragraf."""

html = converter.convert(text)
# <html><head></head><body>
# <h1>Titlul Documentului</h1>
# <p>Primul paragraf cu mai
# multe linii.</p>
# <p>Al doilea paragraf.</p>
# </body></html>
```

#### 1.2 `worker.py` — Clasa `ConverterWorker`

Implementează un `multiprocessing.Process` care:

1. Primește text din `input_queue`
2. Convertește cu `TextToHtmlConverter`
3. Trimite HTML-ul în `output_queue`
4. Se oprește când primește `None` din `input_queue`

```python
import multiprocessing
from lab05.worker import ConverterWorker

input_q = multiprocessing.Queue()
output_q = multiprocessing.Queue()

worker = ConverterWorker(input_q, output_q)
worker.start()

input_q.put("Titlu\n\nParagraf")
rezultat = output_q.get()  # HTML-ul generat
print(rezultat)

input_q.put(None)  # Oprește workerul
worker.join()
```

#### 1.3 `main_window.py` — Clasa `MainWindow`

Implementează fereastra principală cu:

- **Câmp text** + **buton Browse** → deschide dialog pentru selectarea fișierului
- **Buton Upload** → citește fișierul și îl trimite workerului prin coadă
- **QTextEdit** (read-only) → afișează HTML-ul primit de la worker
- **QTimer** → verifică periodic `output_queue` pentru rezultate noi (la 100ms)
- **closeEvent** → trimite `None` în coadă și face `join()` pe worker

### Tema 2 — Joc P2P cu cozi System-V (bonus)

#### 2.1 `game_db.py` — Clasa `GameDatabase`

Implementează operații CRUD în SQLite:

- `insert_score(player: str, score: int)` — inserează scor cu timestamp curent
- `get_scores(player: str)` → lista scorurilor unui jucător
- `get_top_scores(limit: int)` → top scoruri sortate descrescător
- `close()` — închide conexiunea

Schema tabelei `scores`:
```sql
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player TEXT NOT NULL,
    score INTEGER NOT NULL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 2.2 `game.py` — Clasa `Game`

Implementează logica unui joc simplu (ex: Piatră-Hârtie-Foarfecă) cu:

- Comunicare prin cozi System-V (`sysv_ipc` sau alternativă)
- Salvare scor la finalul fiecărei runde
- `send_move(move: str)` și `receive_move() -> str`
- `play_round(my_move: str) -> str` → returnează "win"/"lose"/"draw"

## Exemple de utilizare

### Rulare aplicație:
```bash
uv run python -m lab05.main
```

### Rulare teste:
```bash
uv run pytest
uv run pytest -v tests/test_lab5.py
```

### Testare manuală a converterului:
```python
from lab05.converter import TextToHtmlConverter

c = TextToHtmlConverter()
print(c.convert("Titlu\n\nParagraf 1\n\nParagraf 2"))
```

## Tabel evaluare

| Cerință | Punctaj |
|---------|---------|
| `TextToHtmlConverter.convert()` — titlu h1 | 10p |
| `TextToHtmlConverter.convert()` — paragrafe p | 10p |
| `TextToHtmlConverter.convert()` — text gol | 5p |
| `ConverterWorker` — comunicare prin Queue | 20p |
| `MainWindow` — Browse + Upload funcționale | 20p |
| `MainWindow` — afișare rezultat HTML | 15p |
| `MainWindow` — oprire corectă worker | 10p |
| **Bonus** `GameDatabase` CRUD complet | +10p |
| **Bonus** `Game` — joc P2P funcțional | +10p |
| **Total obligatoriu** | **90p** |
| **Total cu bonus** | **110p** |

## Resurse

- [Documentație PySide6](https://www.riverbankcomputing.com/static/Docs/PySide6/)
- [multiprocessing — Python docs](https://docs.python.org/3/library/multiprocessing.html)
- [sqlite3 — Python docs](https://docs.python.org/3/library/sqlite3.html)
- [QTimer](https://doc.qt.io/qt-5/qtimer.html)
