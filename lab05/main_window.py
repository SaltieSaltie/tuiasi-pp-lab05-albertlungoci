"""
Fereastra principală a aplicației GUI PySide6.

Permite selectarea unui fișier text, trimiterea lui
unui worker prin coadă și afișarea rezultatului HTML.
"""

import multiprocessing

try:
    from PySide6.QtWidgets import (
        QMainWindow,
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QPushButton,
        QLineEdit,
        QTextEdit,
        QFileDialog,
        QLabel,
    )
    from PySide6.QtCore import QTimer
except ImportError:
    # Permite importul fără PySide6 instalat (util în teste)
    QMainWindow = object  # type: ignore[misc, assignment]

from lab05.worker import ConverterWorker


class MainWindow(QMainWindow):
    """Fereastra principală a aplicației de conversie text→HTML."""

    def __init__(self) -> None:
        """Inițializează fereastra și lansează workerul."""
        super().__init__()
        # TODO: Configurează titlul ferestrei și dimensiunea minimă
        # TODO: Creează cozile multiprocessing (input_queue, output_queue)
        # TODO: Pornește ConverterWorker
        # TODO: Construiește UI-ul (apelează _build_ui)
        # TODO: Configurează un QTimer pentru a verifica output_queue periodic
        raise NotImplementedError("De implementat")

    def _build_ui(self) -> None:
        """Construiește interfața grafică.

        Componente necesare:
        - QLabel + QLineEdit pentru calea fișierului
        - QPushButton "Browse" — deschide QFileDialog
        - QPushButton "Upload" — citește fișierul și trimite în coadă
        - QTextEdit (read-only) pentru afișarea HTML-ului rezultat
        """
        # TODO: Implementează layout-ul UI
        raise NotImplementedError("De implementat")

    def _browse_file(self) -> None:
        """Deschide un dialog de selectare fișier și actualizează câmpul de cale."""
        # TODO: Folosește QFileDialog.getOpenFileName
        raise NotImplementedError("De implementat")

    def _upload_file(self) -> None:
        """Citește fișierul selectat și îl trimite în input_queue."""
        # TODO: Citește fișierul, trimite textul în input_queue
        raise NotImplementedError("De implementat")

    def _check_output(self) -> None:
        """Verifică dacă workerul a trimis rezultate în output_queue."""
        # TODO: Citește non-blocant din output_queue și afișează în QTextEdit
        raise NotImplementedError("De implementat")

    def closeEvent(self, event) -> None:  # type: ignore[override]
        """Oprește workerul la închiderea ferestrei."""
        # TODO: Trimite None în input_queue pentru a opri workerul
        # TODO: Așteaptă terminarea procesului worker
        raise NotImplementedError("De implementat")
