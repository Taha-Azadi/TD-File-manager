"""File/Folder properties dialog."""
import os
import platform
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QGridLayout, QFrame,
    QTabWidget, QWidget, QMessageBox
)


class PropertiesDialog(QDialog):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path
        self.setWindowTitle("Properties")
        self.setMinimumWidth(400)

        self._setup_ui()
        self._load_properties()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_edit = QLineEdit()
        self.name_edit.setReadOnly(True)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #ccc;")
        layout.addWidget(line)

        # Properties grid
        grid = QGridLayout()
        grid.setSpacing(8)

        row = 0
        self.labels = {}

        fields = [
            ("Type:", "type"),
            ("Location:", "location"),
            ("Size:", "size"),
            ("Created:", "created"),
            ("Modified:", "modified"),
            ("Accessed:", "accessed"),
        ]

        for label_text, key in fields:
            label = QLabel(label_text)
            value = QLabel("-")
            value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            grid.addWidget(label, row, 0)
            grid.addWidget(value, row, 1)
            self.labels[key] = value
            row += 1

        layout.addLayout(grid)

        # Separator
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setStyleSheet("color: #ccc;")
        layout.addWidget(line2)

        # Attributes
        attr_layout = QHBoxLayout()
        self.attr_readonly = QLabel("Read-only: -")
        self.attr_hidden = QLabel("Hidden: -")
        attr_layout.addWidget(self.attr_readonly)
        attr_layout.addWidget(self.attr_hidden)
        layout.addLayout(attr_layout)

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)

        layout.addLayout(btn_layout)

    def _load_properties(self):
        try:
            stat = os.stat(self.path)
            name = os.path.basename(self.path)

            self.name_edit.setText(name)
            self.labels["location"].setText(os.path.dirname(self.path))

            if os.path.isdir(self.path):
                self.labels["type"].setText("Folder")
                # Calculate folder size
                total_size = self._get_folder_size(self.path)
                self.labels["size"].setText(self._format_size(total_size))
            else:
                ext = os.path.splitext(name)[1].upper()
                self.labels["type"].setText(f"{ext} File" if ext else "File")
                self.labels["size"].setText(self._format_size(stat.st_size))

            self.labels["created"].setText(
                datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            )
            self.labels["modified"].setText(
                datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            )
            self.labels["accessed"].setText(
                datetime.fromtimestamp(stat.st_atime).strftime("%Y-%m-%d %H:%M:%S")
            )

            # Attributes
            self.attr_readonly.setText(f"Read-only: {'Yes' if not os.access(self.path, os.W_OK) else 'No'}")
            self.attr_hidden.setText(f"Hidden: {'Yes' if name.startswith('.') else 'No'}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not load properties:\n{str(e)}")

    def _get_folder_size(self, folder):
        total = 0
        try:
            for entry in os.scandir(folder):
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self._get_folder_size(entry.path)
        except PermissionError:
            pass
        return total

    def _format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                if unit == 'B':
                    return f"{int(size)} {unit}"
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
