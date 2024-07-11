from PySide6.QtWidgets import QApplication
import sys
from MainWindow import MainWindow
from themes import apply_system_theme


def main():
    app = QApplication(sys.argv)

    # Apply system theme
    apply_system_theme(app)

    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
