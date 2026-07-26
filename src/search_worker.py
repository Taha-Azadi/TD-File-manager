"""Background search worker thread."""
import os
from PyQt6.QtCore import QThread, pyqtSignal


class SearchWorker(QThread):
    result_found = pyqtSignal(str)
    finished = pyqtSignal(list)

    def __init__(self, root_path, query, parent=None):
        super().__init__(parent)
        self.root_path = root_path
        self.query = query.lower()
        self._running = True
        self.results = []

    def run(self):
        try:
            for root, dirs, files in os.walk(self.root_path):
                if not self._running:
                    break

                # Skip hidden and system directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]

                for name in dirs + files:
                    if not self._running:
                        break
                    if self.query in name.lower():
                        full_path = os.path.join(root, name)
                        self.results.append(full_path)
                        self.result_found.emit(full_path)
        except PermissionError:
            pass
        except Exception:
            pass

        self.finished.emit(self.results)

    def stop(self):
        self._running = False
        self.wait(1000)
