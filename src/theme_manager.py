"""Theme management for TD File Manager."""
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication


class ThemeManager(QObject):
    theme_changed = pyqtSignal(str)

    LIGHT_STYLESHEET = """
    QMainWindow {
        background-color: #f5f5f5;
    }
    QToolBar {
        background-color: #ffffff;
        border: 1px solid #d4d4d4;
        border-radius: 4px;
        padding: 4px;
        spacing: 4px;
    }
    QToolButton {
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 4px;
        padding: 6px;
        color: #333333;
    }
    QToolButton:hover {
        background-color: #e5e5e5;
        border: 1px solid #cccccc;
    }
    QToolButton:pressed {
        background-color: #d0d0d0;
    }
    QToolButton:disabled {
        color: #aaaaaa;
    }
    QLineEdit {
        background-color: #ffffff;
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 6px;
        color: #333333;
        selection-background-color: #0078d4;
    }
    QLineEdit:focus {
        border: 2px solid #0078d4;
    }
    QTreeView {
        background-color: #ffffff;
        border: none;
        outline: none;
        color: #333333;
    }
    QTreeView::item {
        padding: 4px;
        border-radius: 4px;
    }
    QTreeView::item:selected {
        background-color: #e5f3ff;
        color: #333333;
    }
    QTreeView::item:hover {
        background-color: #f0f0f0;
    }
    QListView {
        background-color: #ffffff;
        border: none;
        outline: none;
        color: #333333;
    }
    QListView::item {
        padding: 4px;
        border-radius: 4px;
    }
    QListView::item:selected {
        background-color: #e5f3ff;
        color: #333333;
    }
    QListView::item:hover {
        background-color: #f0f0f0;
    }
    QTableView {
        background-color: #ffffff;
        border: none;
        gridline-color: #e5e5e5;
        color: #333333;
    }
    QTableView::item {
        padding: 4px;
    }
    QTableView::item:selected {
        background-color: #e5f3ff;
        color: #333333;
    }
    QHeaderView::section {
        background-color: #f5f5f5;
        padding: 6px;
        border: 1px solid #d4d4d4;
        border-left: none;
        font-weight: bold;
        color: #333333;
    }
    QStatusBar {
        background-color: #f0f0f0;
        color: #666666;
        border-top: 1px solid #d4d4d4;
    }
    QMenu {
        background-color: #ffffff;
        border: 1px solid #d4d4d4;
        color: #333333;
        padding: 4px;
    }
    QMenu::item {
        padding: 6px 24px;
        border-radius: 4px;
    }
    QMenu::item:selected {
        background-color: #e5f3ff;
        color: #333333;
    }
    QMenu::separator {
        height: 1px;
        background-color: #e5e5e5;
        margin: 4px 8px;
    }
    QSplitter::handle {
        background-color: #d4d4d4;
    }
    QSplitter::handle:horizontal {
        width: 2px;
    }
    QSplitter::handle:vertical {
        height: 2px;
    }
    QLabel {
        color: #333333;
    }
    QComboBox {
        background-color: #ffffff;
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 4px;
        color: #333333;
    }
    QComboBox:hover {
        border: 1px solid #0078d4;
    }
    QComboBox::drop-down {
        border: none;
        width: 24px;
    }
    QComboBox QAbstractItemView {
        background-color: #ffffff;
        border: 1px solid #d4d4d4;
        selection-background-color: #e5f3ff;
        color: #333333;
    }
    QPushButton {
        background-color: #0078d4;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 6px 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #006cbd;
    }
    QPushButton:pressed {
        background-color: #005a9e;
    }
    QPushButton:disabled {
        background-color: #cccccc;
        color: #888888;
    }
    """

    DARK_STYLESHEET = """
    QMainWindow {
        background-color: #1e1e1e;
    }
    QToolBar {
        background-color: #2d2d2d;
        border: 1px solid #3c3c3c;
        border-radius: 4px;
        padding: 4px;
        spacing: 4px;
    }
    QToolButton {
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 4px;
        padding: 6px;
        color: #cccccc;
    }
    QToolButton:hover {
        background-color: #3c3c3c;
        border: 1px solid #4c4c4c;
    }
    QToolButton:pressed {
        background-color: #505050;
    }
    QToolButton:disabled {
        color: #666666;
    }
    QLineEdit {
        background-color: #2d2d2d;
        border: 1px solid #3c3c3c;
        border-radius: 4px;
        padding: 6px;
        color: #cccccc;
        selection-background-color: #0078d4;
    }
    QLineEdit:focus {
        border: 2px solid #0078d4;
    }
    QTreeView {
        background-color: #1e1e1e;
        border: none;
        outline: none;
        color: #cccccc;
    }
    QTreeView::item {
        padding: 4px;
        border-radius: 4px;
    }
    QTreeView::item:selected {
        background-color: #094771;
        color: #ffffff;
    }
    QTreeView::item:hover {
        background-color: #2a2d2e;
    }
    QListView {
        background-color: #1e1e1e;
        border: none;
        outline: none;
        color: #cccccc;
    }
    QListView::item {
        padding: 4px;
        border-radius: 4px;
    }
    QListView::item:selected {
        background-color: #094771;
        color: #ffffff;
    }
    QListView::item:hover {
        background-color: #2a2d2e;
    }
    QTableView {
        background-color: #1e1e1e;
        border: none;
        gridline-color: #3c3c3c;
        color: #cccccc;
    }
    QTableView::item {
        padding: 4px;
    }
    QTableView::item:selected {
        background-color: #094771;
        color: #ffffff;
    }
    QHeaderView::section {
        background-color: #2d2d2d;
        padding: 6px;
        border: 1px solid #3c3c3c;
        border-left: none;
        font-weight: bold;
        color: #cccccc;
    }
    QStatusBar {
        background-color: #2d2d2d;
        color: #999999;
        border-top: 1px solid #3c3c3c;
    }
    QMenu {
        background-color: #2d2d2d;
        border: 1px solid #3c3c3c;
        color: #cccccc;
        padding: 4px;
    }
    QMenu::item {
        padding: 6px 24px;
        border-radius: 4px;
    }
    QMenu::item:selected {
        background-color: #094771;
        color: #ffffff;
    }
    QMenu::separator {
        height: 1px;
        background-color: #3c3c3c;
        margin: 4px 8px;
    }
    QSplitter::handle {
        background-color: #3c3c3c;
    }
    QSplitter::handle:horizontal {
        width: 2px;
    }
    QSplitter::handle:vertical {
        height: 2px;
    }
    QLabel {
        color: #cccccc;
    }
    QComboBox {
        background-color: #2d2d2d;
        border: 1px solid #3c3c3c;
        border-radius: 4px;
        padding: 4px;
        color: #cccccc;
    }
    QComboBox:hover {
        border: 1px solid #0078d4;
    }
    QComboBox::drop-down {
        border: none;
        width: 24px;
    }
    QComboBox QAbstractItemView {
        background-color: #2d2d2d;
        border: 1px solid #3c3c3c;
        selection-background-color: #094771;
        color: #cccccc;
    }
    QPushButton {
        background-color: #0078d4;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 6px 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #006cbd;
    }
    QPushButton:pressed {
        background-color: #005a9e;
    }
    QPushButton:disabled {
        background-color: #444444;
        color: #888888;
    }
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_theme = "light"

    @property
    def current_theme(self):
        return self._current_theme

    def apply_theme(self, app, theme=None):
        if theme is None:
            theme = self._current_theme
        else:
            self._current_theme = theme

        if theme == "dark":
            app.setStyleSheet(self.DARK_STYLESHEET)
        else:
            app.setStyleSheet(self.LIGHT_STYLESHEET)

        self.theme_changed.emit(theme)

    def toggle_theme(self, app):
        new_theme = "dark" if self._current_theme == "light" else "light"
        self.apply_theme(app, new_theme)
        return new_theme
