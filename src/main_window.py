"""Main window for TD File Manager."""
import os
import sys
import shutil
import subprocess
from pathlib import Path

from PyQt6.QtCore import (
    Qt, QDir, QModelIndex, QItemSelectionModel,
    pyqtSignal, QThread, QTimer, QSize
)
from PyQt6.QtGui import (
    QAction, QKeySequence, QIcon, QCursor,
    QFont, QFontMetrics
)
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTreeView, QTableView, QListView,
    QLineEdit, QLabel, QToolBar, QToolButton,
    QStatusBar, QMenu, QMessageBox, QInputDialog,
    QProgressDialog, QFileDialog, QComboBox,
    QStyledItemDelegate, QHeaderView, QAbstractItemView,
    QApplication, QFrame, QSizePolicy
)

from .file_system_model import CustomFileSystemModel
from .navigation_bar import NavigationBar
from .address_bar import AddressBar
from .search_worker import SearchWorker


class MainWindow(QMainWindow):
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.setWindowTitle("TD File Manager")
        self.setGeometry(100, 100, 1400, 800)

        self.history = []
        self.history_index = -1
        self.max_history = 50

        self.clipboard_operation = None
        self.clipboard_paths = []

        self.view_mode = "details"

        self._setup_model()
        self._setup_ui()
        self._setup_actions()
        self._setup_shortcuts()
        self._connect_signals()

        self.navigate_to(QDir.homePath())

    def _setup_model(self):
        self.model = CustomFileSystemModel()
        self.model.setRootPath("")
        self.model.setReadOnly(False)

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._setup_toolbar()
        layout.addWidget(self.toolbar)

        self._setup_address_search_bar()
        layout.addWidget(self.top_bar_frame)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self._setup_navigation_pane()
        self.splitter.addWidget(self.nav_pane)

        self._setup_content_view()
        self.splitter.addWidget(self.content_widget)

        self.splitter.setSizes([280, 1120])
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        layout.addWidget(self.splitter, 1)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def _setup_toolbar(self):
        self.toolbar = QToolBar("Navigation")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)

        self.btn_back = QToolButton()
        self.btn_back.setText("Back")
        self.btn_back.setToolTip("Back (Alt+Left)")
        self.btn_back.setEnabled(False)
        self.btn_back.clicked.connect(self.go_back)
        self.toolbar.addWidget(self.btn_back)

        self.btn_forward = QToolButton()
        self.btn_forward.setText("Forward")
        self.btn_forward.setToolTip("Forward (Alt+Right)")
        self.btn_forward.setEnabled(False)
        self.btn_forward.clicked.connect(self.go_forward)
        self.toolbar.addWidget(self.btn_forward)

        self.btn_up = QToolButton()
        self.btn_up.setText("Up")
        self.btn_up.setToolTip("Up (Alt+Up)")
        self.btn_up.clicked.connect(self.go_up)
        self.toolbar.addWidget(self.btn_up)

        self.toolbar.addSeparator()

        self.btn_refresh = QToolButton()
        self.btn_refresh.setText("Refresh")
        self.btn_refresh.setToolTip("Refresh (F5)")
        self.btn_refresh.clicked.connect(self.refresh)
        self.toolbar.addWidget(self.btn_refresh)

        self.toolbar.addSeparator()

        self.btn_new_folder = QToolButton()
        self.btn_new_folder.setText("New Folder")
        self.btn_new_folder.setToolTip("New Folder (Ctrl+Shift+N)")
        self.btn_new_folder.clicked.connect(self.create_new_folder)
        self.toolbar.addWidget(self.btn_new_folder)

        self.view_combo = QComboBox()
        self.view_combo.addItems(["Details", "Icons", "List", "Tiles"])
        self.view_combo.setCurrentText("Details")
        self.view_combo.setToolTip("Change View")
        self.view_combo.setFixedWidth(100)
        self.view_combo.currentTextChanged.connect(self.change_view_mode)
        self.toolbar.addWidget(self.view_combo)

        self.toolbar.addSeparator()

        self.btn_theme = QToolButton()
        self.btn_theme.setText("Dark Mode")
        self.btn_theme.setToolTip("Toggle Theme")
        self.btn_theme.clicked.connect(self.toggle_theme)
        self.toolbar.addWidget(self.btn_theme)

    def _setup_address_search_bar(self):
        self.top_bar_frame = QFrame()
        self.top_bar_frame.setFrameShape(QFrame.Shape.StyledPanel)
        top_layout = QHBoxLayout(self.top_bar_frame)
        top_layout.setContentsMargins(8, 4, 8, 4)
        top_layout.setSpacing(8)

        self.address_bar = AddressBar()
        self.address_bar.path_selected.connect(self.navigate_to)
        top_layout.addWidget(self.address_bar, 1)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search current folder...")
        self.search_box.setClearButtonEnabled(True)
        self.search_box.setFixedWidth(250)
        self.search_box.returnPressed.connect(self.perform_search)
        top_layout.addWidget(self.search_box)

    def _setup_navigation_pane(self):
        self.nav_pane = QWidget()
        nav_layout = QVBoxLayout(self.nav_pane)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(""))
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setAnimated(True)
        self.tree_view.setIndentation(16)
        self.tree_view.setUniformRowHeights(True)

        for col in range(1, 4):
            self.tree_view.setColumnHidden(col, True)

        self.tree_view.clicked.connect(self.on_tree_clicked)
        self.tree_view.expanded.connect(self.on_tree_expanded)
        nav_layout.addWidget(self.tree_view)

    def _setup_content_view(self):
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table_view.setColumnWidth(0, 300)
        self.table_view.setColumnWidth(1, 150)
        self.table_view.setColumnWidth(2, 120)
        self.table_view.setColumnWidth(3, 100)
        self.table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.show_context_menu)
        self.table_view.doubleClicked.connect(self.on_item_double_clicked)
        self.table_view.selectionModel().selectionChanged.connect(self.on_selection_changed)

        content_layout.addWidget(self.table_view)

        self.icon_view = QListView()
        self.icon_view.setModel(self.model)
        self.icon_view.setViewMode(QListView.ViewMode.IconMode)
        self.icon_view.setGridSize(QSize(100, 80))
        self.icon_view.setIconSize(QSize(48, 48))
        self.icon_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.icon_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.icon_view.customContextMenuRequested.connect(self.show_context_menu)
        self.icon_view.doubleClicked.connect(self.on_item_double_clicked)
        self.icon_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.icon_view.hide()
        content_layout.addWidget(self.icon_view)

        self.list_view = QListView()
        self.list_view.setModel(self.model)
        self.list_view.setViewMode(QListView.ViewMode.ListMode)
        self.list_view.setIconSize(QSize(24, 24))
        self.list_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.show_context_menu)
        self.list_view.doubleClicked.connect(self.on_item_double_clicked)
        self.list_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.list_view.hide()
        content_layout.addWidget(self.list_view)

    def _setup_actions(self):
        self.act_new_folder = QAction("New Folder", self)
        self.act_new_folder.setShortcut(QKeySequence("Ctrl+Shift+N"))
        self.act_new_folder.triggered.connect(self.create_new_folder)

        self.act_refresh = QAction("Refresh", self)
        self.act_refresh.setShortcut(QKeySequence("F5"))
        self.act_refresh.triggered.connect(self.refresh)

        self.act_exit = QAction("Exit", self)
        self.act_exit.setShortcut(QKeySequence("Alt+F4"))
        self.act_exit.triggered.connect(self.close)

        self.act_cut = QAction("Cut", self)
        self.act_cut.setShortcut(QKeySequence("Ctrl+X"))
        self.act_cut.triggered.connect(self.cut_selected)

        self.act_copy = QAction("Copy", self)
        self.act_copy.setShortcut(QKeySequence("Ctrl+C"))
        self.act_copy.triggered.connect(self.copy_selected)

        self.act_paste = QAction("Paste", self)
        self.act_paste.setShortcut(QKeySequence("Ctrl+V"))
        self.act_paste.triggered.connect(self.paste)

        self.act_delete = QAction("Delete", self)
        self.act_delete.setShortcut(QKeySequence("Delete"))
        self.act_delete.triggered.connect(self.delete_selected)

        self.act_rename = QAction("Rename", self)
        self.act_rename.setShortcut(QKeySequence("F2"))
        self.act_rename.triggered.connect(self.rename_selected)

        self.act_details = QAction("Details", self)
        self.act_details.setCheckable(True)
        self.act_details.setChecked(True)
        self.act_details.triggered.connect(lambda: self.set_view_mode("details"))

        self.act_icons = QAction("Icons", self)
        self.act_icons.setCheckable(True)
        self.act_icons.triggered.connect(lambda: self.set_view_mode("icons"))

        self.act_list = QAction("List", self)
        self.act_list.setCheckable(True)
        self.act_list.triggered.connect(lambda: self.set_view_mode("list"))

        self.act_tiles = QAction("Tiles", self)
        self.act_tiles.setCheckable(True)
        self.act_tiles.triggered.connect(lambda: self.set_view_mode("tiles"))

        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.act_new_folder)
        file_menu.addSeparator()
        file_menu.addAction(self.act_refresh)
        file_menu.addSeparator()
        file_menu.addAction(self.act_exit)

        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction(self.act_cut)
        edit_menu.addAction(self.act_copy)
        edit_menu.addAction(self.act_paste)
        edit_menu.addSeparator()
        edit_menu.addAction(self.act_delete)
        edit_menu.addAction(self.act_rename)

        view_menu = menubar.addMenu("View")
        view_menu.addAction(self.act_details)
        view_menu.addAction(self.act_icons)
        view_menu.addAction(self.act_list)
        view_menu.addAction(self.act_tiles)

    def _setup_shortcuts(self):
        shortcut_up = QAction(self)
        shortcut_up.setShortcut(QKeySequence("Alt+Up"))
        shortcut_up.triggered.connect(self.go_up)
        self.addAction(shortcut_up)

        shortcut_back = QAction(self)
        shortcut_back.setShortcut(QKeySequence("Alt+Left"))
        shortcut_back.triggered.connect(self.go_back)
        self.addAction(shortcut_back)

        shortcut_forward = QAction(self)
        shortcut_forward.setShortcut(QKeySequence("Alt+Right"))
        shortcut_forward.triggered.connect(self.go_forward)
        self.addAction(shortcut_forward)

        shortcut_select_all = QAction(self)
        shortcut_select_all.setShortcut(QKeySequence("Ctrl+A"))
        shortcut_select_all.triggered.connect(self.select_all)
        self.addAction(shortcut_select_all)

    def _connect_signals(self):
        self.model.directoryLoaded.connect(self.on_directory_loaded)

    def navigate_to(self, path):
        path = os.path.normpath(path)
        if not os.path.exists(path):
            QMessageBox.warning(self, "Error", f"Path does not exist:\n{path}")
            return

        if self.history_index < 0 or self.history[self.history_index] != path:
            self.history = self.history[:self.history_index + 1]
            self.history.append(path)
            if len(self.history) > self.max_history:
                self.history.pop(0)
            self.history_index = len(self.history) - 1

        self._update_navigation_ui()
        self._set_root_index(path)
        self.address_bar.set_path(path)
        self.search_box.clear()

    def _set_root_index(self, path):
        index = self.model.index(path)
        self.table_view.setRootIndex(index)
        self.icon_view.setRootIndex(index)
        self.list_view.setRootIndex(index)
        self._expand_tree_to_path(path)

    def _expand_tree_to_path(self, path):
        parts = Path(path).parts
        current = ""
        for part in parts:
            current = os.path.join(current, part) if current else part
            if os.name == "nt" and len(current) == 2 and current[1] == ":":
                current = current + os.sep
            idx = self.model.index(current)
            if idx.isValid():
                self.tree_view.expand(idx)
                self.tree_view.setCurrentIndex(idx)

    def _update_navigation_ui(self):
        self.btn_back.setEnabled(self.history_index > 0)
        self.btn_forward.setEnabled(self.history_index < len(self.history) - 1)

        current_path = self.history[self.history_index] if self.history_index >= 0 else ""
        parent = os.path.dirname(current_path)
        self.btn_up.setEnabled(parent != current_path and current_path != "")

    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            path = self.history[self.history_index]
            self._update_navigation_ui()
            self._set_root_index(path)
            self.address_bar.set_path(path)

    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            path = self.history[self.history_index]
            self._update_navigation_ui()
            self._set_root_index(path)
            self.address_bar.set_path(path)

    def go_up(self):
        if self.history_index >= 0:
            current = self.history[self.history_index]
            parent = os.path.dirname(current)
            if parent != current:
                self.navigate_to(parent)

    def refresh(self):
        self.model.refresh()
        if self.history_index >= 0:
            self._set_root_index(self.history[self.history_index])

    def on_tree_clicked(self, index):
        path = self.model.filePath(index)
        if os.path.isdir(path):
            self.navigate_to(path)

    def on_tree_expanded(self, index):
        self.tree_view.resizeColumnToContents(0)

    def on_item_double_clicked(self, index):
        path = self.model.filePath(index)
        if os.path.isdir(path):
            self.navigate_to(path)
        else:
            self.open_file(path)

    def open_file(self, path):
        try:
            if os.name == "nt":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.run(["open", path], check=True)
            else:
                subprocess.run(["xdg-open", path], check=True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open file:\n{str(e)}")

    def on_selection_changed(self):
        view = self._get_active_view()
        selected = view.selectionModel().selectedRows() if hasattr(view, 'selectionModel') else []

        if not selected:
            current = self.history[self.history_index] if self.history_index >= 0 else ""
            if current and os.path.isdir(current):
                try:
                    items = os.listdir(current)
                    files = [f for f in items if os.path.isfile(os.path.join(current, f))]
                    dirs = [f for f in items if os.path.isdir(os.path.join(current, f))]
                    msg = f"{len(dirs)} folder(s), {len(files)} file(s)"
                except PermissionError:
                    msg = "Access denied"
            else:
                msg = "Ready"
        else:
            count = len(selected)
            if count == 1:
                path = self.model.filePath(selected[0])
                msg = f"Selected: {os.path.basename(path)}"
            else:
                msg = f"{count} items selected"

        self.status_bar.showMessage(msg)

    def on_directory_loaded(self, path):
        self.on_selection_changed()

    def _get_active_view(self):
        if self.view_mode == "details":
            return self.table_view
        elif self.view_mode == "icons":
            return self.icon_view
        elif self.view_mode in ("list", "tiles"):
            return self.list_view
        return self.table_view

    def change_view_mode(self, mode_text):
        mode_map = {
            "Details": "details",
            "Icons": "icons",
            "List": "list",
            "Tiles": "tiles"
        }
        self.set_view_mode(mode_map.get(mode_text, "details"))

    def set_view_mode(self, mode):
        self.view_mode = mode

        self.table_view.hide()
        self.icon_view.hide()
        self.list_view.hide()

        self.act_details.setChecked(mode == "details")
        self.act_icons.setChecked(mode == "icons")
        self.act_list.setChecked(mode == "list")
        self.act_tiles.setChecked(mode == "tiles")

        mode_text_map = {
            "details": "Details",
            "icons": "Icons",
            "list": "List",
            "tiles": "Tiles"
        }
        self.view_combo.setCurrentText(mode_text_map.get(mode, "Details"))

        if mode == "details":
            self.table_view.show()
        elif mode == "icons":
            self.icon_view.setViewMode(QListView.ViewMode.IconMode)
            self.icon_view.setGridSize(QSize(100, 90))
            self.icon_view.setIconSize(QSize(64, 64))
            self.icon_view.show()
        elif mode == "list":
            self.list_view.setViewMode(QListView.ViewMode.ListMode)
            self.list_view.setIconSize(QSize(24, 24))
            self.list_view.show()
        elif mode == "tiles":
            self.icon_view.setViewMode(QListView.ViewMode.ListMode)
            self.icon_view.setIconSize(QSize(48, 48))
            self.icon_view.show()

    def show_context_menu(self, position):
        view = self._get_active_view()
        index = view.indexAt(position)

        menu = QMenu(self)

        if index.isValid():
            path = self.model.filePath(index)

            act_open = menu.addAction("Open")
            act_open.triggered.connect(lambda: self.on_item_double_clicked(index))
            menu.addSeparator()

            act_cut = menu.addAction("Cut")
            act_cut.triggered.connect(self.cut_selected)
            act_copy = menu.addAction("Copy")
            act_copy.triggered.connect(self.copy_selected)
            menu.addSeparator()

            act_rename = menu.addAction("Rename")
            act_rename.triggered.connect(self.rename_selected)
            act_delete = menu.addAction("Delete")
            act_delete.triggered.connect(self.delete_selected)
            menu.addSeparator()

            act_props = menu.addAction("Properties")
            act_props.triggered.connect(lambda: self.show_properties(path))
        else:
            act_paste = menu.addAction("Paste")
            act_paste.triggered.connect(self.paste)
            act_paste.setEnabled(len(self.clipboard_paths) > 0)
            menu.addSeparator()

            act_new = menu.addAction("New Folder")
            act_new.triggered.connect(self.create_new_folder)
            menu.addSeparator()

            act_refresh_ctx = menu.addAction("Refresh")
            act_refresh_ctx.triggered.connect(self.refresh)

        menu.exec(QCursor.pos())

    def select_all(self):
        view = self._get_active_view()
        view.selectAll()

    def create_new_folder(self):
        current = self.history[self.history_index] if self.history_index >= 0 else QDir.homePath()

        name, ok = QInputDialog.getText(
            self, "New Folder", "Folder name:",
            text="New Folder"
        )
        if ok and name:
            new_path = os.path.join(current, name)
            try:
                os.makedirs(new_path, exist_ok=False)
                self.refresh()
            except FileExistsError:
                QMessageBox.warning(self, "Error", f"A folder named '{name}' already exists.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not create folder:\n{str(e)}")

    def cut_selected(self):
        view = self._get_active_view()
        selected = view.selectionModel().selectedRows() if hasattr(view, 'selectionModel') else []
        if not selected:
            selected = view.selectionModel().selectedIndexes()

        self.clipboard_paths = [self.model.filePath(idx) for idx in selected]
        self.clipboard_operation = "cut"
        self.status_bar.showMessage(f"Cut {len(self.clipboard_paths)} item(s)")

    def copy_selected(self):
        view = self._get_active_view()
        selected = view.selectionModel().selectedRows() if hasattr(view, 'selectionModel') else []
        if not selected:
            selected = view.selectionModel().selectedIndexes()

        self.clipboard_paths = [self.model.filePath(idx) for idx in selected]
        self.clipboard_operation = "copy"
        self.status_bar.showMessage(f"Copied {len(self.clipboard_paths)} item(s)")

    def paste(self):
        if not self.clipboard_paths:
            return

        current = self.history[self.history_index] if self.history_index >= 0 else QDir.homePath()

        for src in self.clipboard_paths:
            if not os.path.exists(src):
                continue

            basename = os.path.basename(src)
            dst = os.path.join(current, basename)

            counter = 1
            while os.path.exists(dst):
                name, ext = os.path.splitext(basename)
                dst = os.path.join(current, f"{name} ({counter}){ext}")
                counter += 1

            try:
                if self.clipboard_operation == "cut":
                    shutil.move(src, dst)
                else:
                    if os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Operation failed:\n{str(e)}")

        if self.clipboard_operation == "cut":
            self.clipboard_paths = []
            self.clipboard_operation = None

        self.refresh()

    def delete_selected(self):
        view = self._get_active_view()
        selected = view.selectionModel().selectedRows() if hasattr(view, 'selectionModel') else []
        if not selected:
            selected = view.selectionModel().selectedIndexes()

        if not selected:
            return

        paths = [self.model.filePath(idx) for idx in selected]
        names = [os.path.basename(p) for p in paths]

        if len(names) == 1:
            msg = f"Are you sure you want to delete '{names[0]}'?"
        else:
            msg = f"Are you sure you want to delete {len(names)} items?"

        reply = QMessageBox.question(
            self, "Confirm Delete", msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            for path in paths:
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Could not delete '{os.path.basename(path)}':\n{str(e)}")
            self.refresh()

    def rename_selected(self):
        view = self._get_active_view()
        selected = view.selectionModel().selectedRows() if hasattr(view, 'selectionModel') else []
        if not selected:
            selected = view.selectionModel().selectedIndexes()

        if not selected:
            return

        index = selected[0]
        path = self.model.filePath(index)
        old_name = os.path.basename(path)

        new_name, ok = QInputDialog.getText(
            self, "Rename", "New name:", text=old_name
        )
        if ok and new_name and new_name != old_name:
            new_path = os.path.join(os.path.dirname(path), new_name)
            try:
                os.rename(path, new_path)
                self.refresh()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not rename:\n{str(e)}")

    def show_properties(self, path):
        from .properties_dialog import PropertiesDialog
        dialog = PropertiesDialog(path, self)
        dialog.exec()

    def perform_search(self):
        query = self.search_box.text().strip()
        if not query:
            return

        current = self.history[self.history_index] if self.history_index >= 0 else QDir.homePath()

        self.progress = QProgressDialog("Searching...", "Cancel", 0, 0, self)
        self.progress.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress.setWindowTitle("Search")
        self.progress.show()

        self.search_worker = SearchWorker(current, query)
        self.search_worker.result_found.connect(self.on_search_result)
        self.search_worker.finished.connect(self.on_search_finished)
        self.search_worker.start()

        self.progress.canceled.connect(self.search_worker.stop)

    def on_search_result(self, path):
        pass

    def on_search_finished(self, results):
        self.progress.close()
        if results:
            msg = f"Found {len(results)} result(s):\n\n"
            msg += "\n".join(results[:20])
            if len(results) > 20:
                msg += f"\n... and {len(results) - 20} more"
            QMessageBox.information(self, "Search Results", msg)
        else:
            QMessageBox.information(self, "Search Results", "No results found.")

    def toggle_theme(self):
        new_theme = self.theme_manager.toggle_theme(QApplication.instance())
        self.btn_theme.setText("Light Mode" if new_theme == "dark" else "Dark Mode")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        current = self.history[self.history_index] if self.history_index >= 0 else QDir.homePath()

        for url in urls:
            src = url.toLocalFile()
            if src:
                dst = os.path.join(current, os.path.basename(src))
                try:
                    if os.path.isdir(src):
                        if os.path.exists(dst):
                            shutil.rmtree(dst)
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Could not copy '{os.path.basename(src)}':\n{str(e)}")
        self.refresh()
