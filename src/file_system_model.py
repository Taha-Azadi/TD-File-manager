"""Custom file system model with enhanced features."""
import os
from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QFileSystemModel


class CustomFileSystemModel(QFileSystemModel):
    """Enhanced file system model with custom display and sorting."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFilter(QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot | QDir.Filter.Hidden)
        self.setNameFilterDisables(False)

    def refresh(self):
        """Refresh the model by re-setting root path."""
        root = self.rootPath()
        self.setRootPath("")
        self.setRootPath(root)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if column == 1:  # Date Modified
                file_info = self.fileInfo(index)
                date_time = file_info.lastModified()
                return date_time.toString("yyyy-MM-dd HH:mm")
            elif column == 2:  # Type
                file_info = self.fileInfo(index)
                if file_info.isDir():
                    return "Folder"
                suffix = file_info.suffix().upper()
                if suffix:
                    return f"{suffix} File"
                return "File"
            elif column == 3:  # Size
                file_info = self.fileInfo(index)
                if file_info.isDir():
                    return ""
                size = file_info.size()
                return self._format_size(size)

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if column == 3:  # Size right-aligned
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

        return super().data(index, role)

    def _format_size(self, size):
        """Format byte size to human readable string."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                if unit == 'B':
                    return f"{int(size)} {unit}"
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            headers = ["Name", "Date Modified", "Type", "Size"]
            if section < len(headers):
                return headers[section]
        return super().headerData(section, orientation, role)

    def sort(self, column, order):
        """Custom sorting logic."""
        self.layoutAboutToBeChanged.emit()
        super().sort(column, order)
        self.layoutChanged.emit()
