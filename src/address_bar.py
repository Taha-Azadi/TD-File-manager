"""Address bar with breadcrumb navigation."""
import os
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QLineEdit,
    QToolButton, QFrame, QSizePolicy
)


class AddressBar(QWidget):
    path_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_path = ""
        self._edit_mode = False

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(4, 2, 4, 2)
        self.layout.setSpacing(2)

        # Breadcrumb container
        self.breadcrumb_frame = QFrame()
        self.breadcrumb_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.breadcrumb_layout = QHBoxLayout(self.breadcrumb_frame)
        self.breadcrumb_layout.setContentsMargins(4, 2, 4, 2)
        self.breadcrumb_layout.setSpacing(0)
        self.breadcrumb_layout.addStretch()

        # Edit mode line edit
        self.path_edit = QLineEdit()
        self.path_edit.setFrame(False)
        self.path_edit.returnPressed.connect(self._on_edit_confirmed)
        self.path_edit.editingFinished.connect(self._on_edit_finished)
        self.path_edit.hide()

        self.layout.addWidget(self.breadcrumb_frame, 1)
        self.layout.addWidget(self.path_edit, 1)

        self.set_path(os.path.expanduser("~"))

    def set_path(self, path):
        self._current_path = path
        if not self._edit_mode:
            self._update_breadcrumb()
        self.path_edit.setText(path)

    def _update_breadcrumb(self):
        # Clear existing breadcrumbs
        while self.breadcrumb_layout.count() > 1:
            item = self.breadcrumb_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        parts = []
        current = self._current_path

        # Handle Windows drives
        if os.name == "nt" and len(current) >= 2 and current[1] == ":":
            parts.append(current[:2] + os.sep)
            current = current[3:] if len(current) > 3 else ""
        elif current.startswith("/"):
            parts.append("/")
            current = current[1:]

        if current:
            parts.extend(current.split(os.sep))

        # Build path progressively
        build_path = ""
        for i, part in enumerate(parts):
            if i == 0:
                build_path = part
            else:
                build_path = os.path.join(build_path, part)

            btn = QToolButton()
            btn.setText(part if part else "/")
            btn.setStyleSheet("""
                QToolButton {
                    border: none;
                    padding: 2px 6px;
                    background: transparent;
                }
                QToolButton:hover {
                    background: #e5f3ff;
                    border-radius: 3px;
                }
            """)
            btn.setProperty("path", build_path)
            btn.clicked.connect(self._on_breadcrumb_clicked)
            self.breadcrumb_layout.insertWidget(self.breadcrumb_layout.count() - 1, btn)

            if i < len(parts) - 1:
                sep = QLabel(">")
                sep.setStyleSheet("color: #888; padding: 0 2px;")
                self.breadcrumb_layout.insertWidget(self.breadcrumb_layout.count() - 1, sep)

    def _on_breadcrumb_clicked(self):
        btn = self.sender()
        path = btn.property("path")
        if path:
            self.path_selected.emit(path)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self._edit_mode:
            if self.breadcrumb_frame.geometry().contains(event.pos()):
                self._enter_edit_mode()
        super().mousePressEvent(event)

    def _enter_edit_mode(self):
        self._edit_mode = True
        self.breadcrumb_frame.hide()
        self.path_edit.show()
        self.path_edit.setFocus()
        self.path_edit.selectAll()

    def _exit_edit_mode(self):
        self._edit_mode = False
        self.path_edit.hide()
        self.breadcrumb_frame.show()
        self._update_breadcrumb()

    def _on_edit_confirmed(self):
        path = self.path_edit.text().strip()
        if path:
            self.path_selected.emit(path)
        self._exit_edit_mode()

    def _on_edit_finished(self):
        if self._edit_mode:
            self._exit_edit_mode()
