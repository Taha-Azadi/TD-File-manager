<div align="center">

<!-- Animated Header -->
[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=30&duration=3000&pause=1000&color=3B8ED0&center=true&vCenter=true&width=600&lines=TD+File+Manager+v1.0.0;Modern+%7C+Fast+%7C+Cross-Platform;Windows-Style+File+Explorer)](https://github.com/Taha-Azadi/TD-File-manager)

<!-- Badges -->
<p>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://www.riverbankcomputing.com/software/pyqt/"><img src="https://img.shields.io/badge/PyQt6-6.4%2B-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"></a>
  <a href="#"><img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-4B0082?style=for-the-badge" alt="Platform"></a>
</p>

<!-- Banner Image -->
<img src="screenshots/banner.png" alt="TD File Manager Banner" width="900"/>

<p><b>A powerful, modern file manager inspired by Windows Explorer — built with Python & PyQt6.</b></p>

<p>
  <a href="#features">Features</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#keyboard-shortcuts">Shortcuts</a> •
  <a href="#tech-stack">Tech Stack</a>
</p>

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🗂️ Dual-Pane Layout
- **Left Panel**: Hierarchical tree navigation with expandable folders
- **Right Panel**: Content view with 4 different display modes
- **Resizable Splitter**: Adjust panel widths to your preference

### 🔗 Smart Address Bar
- **Breadcrumb Navigation**: Click any folder in the path to jump directly
- **Edit Mode**: Click the path to type a full directory path manually
- **Auto-Updates**: Path bar syncs automatically as you browse

### 👁️ Multiple View Modes
| Mode | Description |
|------|-------------|
| 📋 **Details** | Column view — Name, Date, Type, Size with sorting |
| 🖼️ **Icons** | Large icon grid for visual browsing |
| 📑 **List** | Compact list with small icons |
| 🟦 **Tiles** | Medium icons with file names |

</td>
<td width="50%">

### ✂️ Full File Operations
- **Cut / Copy / Paste** with clipboard persistence
- **Delete** with confirmation dialog
- **Rename** inline or via dialog (F2)
- **New Folder** creation (Ctrl+Shift+N)
- **Drag & Drop** support for importing files

### 🔍 Built-in Search
- Search within current directory recursively
- Background threaded search (no UI freeze)
- Progress dialog with cancel option
- Results displayed with full paths

### 🌗 Light & Dark Themes
- **Light Mode**: Clean, modern Windows-style white theme
- **Dark Mode**: Eye-friendly dark theme for night usage
- **One-click toggle** with persistent state
- Custom stylesheet engine for consistent styling

</td>
</tr>
</table>

---

## 📸 Screenshots

### 🖥️ Main Interface — Light Mode
<p align="center">
  <img src="screenshots/light_mode_main.png" alt="Light Mode Main Interface" width="900"/>
</p>
<p align="center"><i>Main window showing dual-pane layout with Details view in Light theme</i></p>

### 🌙 Main Interface — Dark Mode
<p align="center">
  <img src="screenshots/dark_mode_main.png" alt="Dark Mode Main Interface" width="900"/>
</p>
<p align="center"><i>Same view with Dark theme enabled — easy on the eyes for night sessions</i></p>

### 🖼️ Icons View
<p align="center">
  <img src="screenshots/view_icons.png" alt="Icons View" width="900"/>
</p>
<p align="center"><i>Large icon grid view for visual file browsing</i></p>

### 📑 List & Tiles View
<p align="center">
  <img src="screenshots/view_list_tiles.png" alt="List and Tiles View" width="900"/>
</p>
<p align="center"><i>Compact List view (left) and Tiles view (right)</i></p>

### 🔍 Search in Action
<p align="center">
  <img src="screenshots/search_feature.png" alt="Search Feature" width="700"/>
</p>
<p align="center"><i>Real-time search with progress dialog and result listing</i></p>

### 📋 Context Menu & Properties
<p align="center">
  <img src="screenshots/context_menu.png" alt="Context Menu" width="400"/>
  &nbsp;&nbsp;
  <img src="screenshots/properties_dialog.png" alt="Properties Dialog" width="400"/>
</p>
<p align="center"><i>Right-click context menu (left) and File Properties dialog (right)</i></p>

### 🗂️ Breadcrumb Navigation
<p align="center">
  <img src="screenshots/breadcrumb_bar.png" alt="Breadcrumb Address Bar" width="800"/>
</p>
<p align="center"><i>Clickable breadcrumb path bar — jump to any parent folder instantly</i></p>

---

## 🚀 Installation

### Prerequisites
- Python **3.9** or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Taha-Azadi/TD-File-manager.git
cd TD-File-manager
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run
```bash
python main.py
```

---

## 🎮 Usage

### Basic Navigation
- Click folders in the **left tree** or **right pane** to navigate
- Use **Back / Forward / Up** buttons or `Alt+Arrow` keys
- Click any part of the **breadcrumb path** to jump to that folder

### File Operations
| Action | How |
|--------|-----|
| Open file/folder | Double-click or Enter |
| New Folder | Toolbar button or `Ctrl+Shift+N` |
| Rename | `F2` or right-click → Rename |
| Delete | `Delete` key or right-click → Delete |
| Cut / Copy / Paste | `Ctrl+X/C/V` or context menu |

### Switching Views
Use the **View dropdown** in the toolbar or the **View menu**:
- **Details** — Sortable columns, best for file management
- **Icons** — Best for folders with images
- **List** — Compact, maximum items visible
- **Tiles** — Balanced icon + name display

### Themes
Click the **Dark Mode / Light Mode** button in the toolbar to toggle instantly.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Alt + Left` | Go Back |
| `Alt + Right` | Go Forward |
| `Alt + Up` | Go to Parent Folder |
| `F5` | Refresh |
| `Ctrl + Shift + N` | New Folder |
| `Ctrl + X` | Cut |
| `Ctrl + C` | Copy |
| `Ctrl + V` | Paste |
| `Delete` | Delete (with confirmation) |
| `F2` | Rename |
| `Ctrl + A` | Select All |

---

## 🛠 Tech Stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,qt,git,github,vscode&theme=dark" />
</p>

| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Core language |
| **PyQt6** | Cross-platform GUI framework |
| **QFileSystemModel** | Native file system integration & caching |
| **QThread** | Background search without blocking UI |
| **Custom Stylesheets** | Light/Dark theme engine |

---

## 📁 Project Structure

```
TD-File-manager/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
├── README.md                    # This file
├── screenshots/                 # App screenshots
│   ├── banner.png
│   ├── light_mode_main.png
│   ├── dark_mode_main.png
│   ├── view_icons.png
│   ├── view_list_tiles.png
│   ├── search_feature.png
│   ├── context_menu.png
│   ├── properties_dialog.png
│   └── breadcrumb_bar.png
├── src/                         # Source code
│   ├── __init__.py
│   ├── main_window.py          # Main window & UI logic
│   ├── file_system_model.py    # Custom QFileSystemModel
│   ├── address_bar.py          # Breadcrumb address bar
│   ├── theme_manager.py        # Light/Dark theme engine
│   ├── search_worker.py        # Background search thread
│   ├── properties_dialog.py    # File properties dialog
│   └── navigation_bar.py       # Navigation components
└── docs/
    └── usage.md                # Extended usage documentation
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. Create a **feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit** your changes: `git commit -m 'Add some AmazingFeature'`
4. **Push** to the branch: `git push origin feature/AmazingFeature`
5. Open a **Pull Request**

### Priority Contributions
- [ ] Add **thumbnail previews** for images in Icon view
- [ ] Add **file preview pane** (text, images, PDF)
- [ ] Implement **multi-tab browsing**
- [ ] Add **bookmark/favorites** sidebar section
- [ ] Implement **file compression** (ZIP/RAR creation)
- [ ] Add **bulk rename** tool

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

## 👨‍💻 Built by [Taha Azadi](https://github.com/Taha-Azadi)

<p>
  <a href="https://github.com/Taha-Azadi"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="https://x.com/TahaAzadiDev"><img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter"></a>
  <a href="https://www.linkedin.com/in/Taha-Azadi-Dev"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:taha.azadi.dev@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
</p>

<p><i>Building practical tools with clean code. From Zanjan to the world.</i></p>

<!-- Profile views counter -->
<p>
  <img src="https://komarev.com/ghpvc/?username=Taha-Azadi&color=3B8ED0&style=flat-square" alt="Profile Views" />
</p>

</div>
