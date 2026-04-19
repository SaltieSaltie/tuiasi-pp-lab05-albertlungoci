"""
Entry point pentru aplicația de conversie text→HTML.

Utilizare:
    uv run python -m lab05.main
"""

import sys

try:
    from PySide6.QtWidgets import QApplication
    from lab05.main_window import MainWindow

    def main() -> None:
        """Pornește aplicația PySide6."""
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

except ImportError as e:
    def main() -> None:  # type: ignore[misc]
        print(f"Eroare: PySide6 nu este instalat. {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
