import sys

from PySide6.QtWidgets import QApplication

from text_comparator.diff_viewer import MainWindow


def cli():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    cli()
