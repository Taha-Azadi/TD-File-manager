import sys
from PyQt6.QtWidgets import QApplication
from src.main_window import MainWindow
from src.theme_manager import ThemeManager


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("TD File Manager")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Taha-Azadi")

    # Initialize theme
    theme_manager = ThemeManager()
    theme_manager.apply_theme(app)

    window = MainWindow(theme_manager)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
