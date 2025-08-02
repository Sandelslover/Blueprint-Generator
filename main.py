import os
import json
import sys
import time
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
    QPushButton, QLabel, QLineEdit, QTreeWidget, QTreeWidgetItem, QMenu,
    QFileDialog, QMessageBox, QFrame, QInputDialog, QSplitter, QTextEdit,
    QGroupBox, QCheckBox, QSpinBox, QTabWidget, QScrollArea, QListWidget,
    QProgressBar, QStatusBar, QToolTip, QSystemTrayIcon
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, pyqtSignal, QThread, QTimer, QSettings, QMimeData
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QLinearGradient, QKeySequence, QDragEnterEvent, QDropEvent, QAction, QShortcut

class ProjectCreationThread(QThread):
    """Background thread for project creation with progress updates"""
    progress_updated = pyqtSignal(int, str)
    creation_finished = pyqtSignal(bool, str)
    
    def __init__(self, creator, preset_name, project_path):
        super().__init__()
        self.creator = creator
        self.preset_name = preset_name
        self.project_path = project_path
    
    def run(self):
        try:
            self.progress_updated.emit(10, "Preparing project structure...")
            time.sleep(0.2)  # Small delay for visual feedback
            
            self.progress_updated.emit(30, "Creating directories...")
            success = self.creator.create_project_with_progress(
                self.preset_name, self.project_path, self.progress_updated
            )
            
            if success:
                self.progress_updated.emit(100, "Project created successfully!")
                self.creation_finished.emit(True, "Project structure created successfully!")
            else:
                self.creation_finished.emit(False, "Template not found!")
        except Exception as e:
            self.creation_finished.emit(False, f"Failed to create project: {str(e)}")

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None, tooltip=None):
        super().__init__(text, parent)
        if tooltip:
            self.setToolTip(tooltip)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5ba0f2, stop:1 #4080cd);
                border: 2px solid #ffffff40;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a80d2, stop:1 #2570ad);
                padding: 13px 23px 11px 25px;
            }
            QPushButton:disabled {
                background: #555;
                color: #999;
            }
        """)

class ProjectStructureCreator:
    def __init__(self):
        self.presets_file = "presets.json"
        self.presets = self.load_presets()

    def load_presets(self):
        """Load presets from JSON file or return default presets if file doesn't exist."""
        default_presets = {
            "react-app": {
                "public": {
                    "images": {},
                    "css": {},
                    "favicon.ico": None
                },
                "src": {
                    "components": {
                        "common": {},
                        "layout": {}
                    },
                    "pages": {},
                    "hooks": {},
                    "context": {},
                    "services": {
                        "api": {}
                    },
                    "utils": {},
                    "styles": {
                        "components": {},
                        "globals.css": None
                    },
                    "assets": {
                        "images": {},
                        "icons": {}
                    }
                },
                "tests": {
                    "unit": {},
                    "integration": {},
                    "__mocks__": {}
                },
                "config": {
                    "webpack.config.js": None
                },
                "scripts": {
                    "build.sh": None,
                    "deploy.sh": None
                },
                "docs": {
                    "api.md": None,
                    "components.md": None
                },
                "node_modules": {},
                "dist": {},
                ".gitignore": None,
                "package.json": None,
                "README.md": None,
                ".env": None,
                ".env.example": None,
                ".eslintrc.js": None,
                "vite.config.js": None,
                "tsconfig.json": None
            },
            "nextjs-app": {
                "app": {
                    "api": {},
                    "globals.css": None,
                    "layout.tsx": None,
                    "loading.tsx": None,
                    "page.tsx": None
                },
                "components": {
                    "ui": {},
                    "forms": {},
                    "layout": {}
                },
                "lib": {
                    "utils.ts": None,
                    "validations.ts": None
                },
                "hooks": {},
                "types": {
                    "index.ts": None
                },
                "public": {
                    "images": {},
                    "icons": {}
                },
                "styles": {},
                "tests": {
                    "__mocks__": {}
                },
                "docs": {},
                "node_modules": {},
                ".next": {},
                ".gitignore": None,
                "package.json": None,
                "README.md": None,
                ".env.local": None,
                "next.config.js": None,
                "tailwind.config.js": None,
                "tsconfig.json": None
            },
            "express-api": {
                "src": {
                    "controllers": {},
                    "routes": {
                        "api": {}
                    },
                    "models": {},
                    "middleware": {
                        "auth.js": None,
                        "validation.js": None
                    },
                    "services": {},
                    "utils": {
                        "logger.js": None,
                        "database.js": None
                    },
                    "config": {
                        "database.js": None,
                        "cors.js": None
                    }
                },
                "tests": {
                    "unit": {},
                    "integration": {},
                    "e2e": {}
                },
                "migrations": {},
                "seeders": {},
                "public": {
                    "uploads": {}
                },
                "logs": {},
                "scripts": {
                    "seed.js": None,
                    "migrate.js": None
                },
                "docs": {
                    "swagger.yaml": None,
                    "api.md": None
                },
                "node_modules": {},
                ".gitignore": None,
                "package.json": None,
                "README.md": None,
                ".env": None,
                ".env.example": None,
                ".eslintrc.js": None,
                "jest.config.js": None,
                "Dockerfile": None,
                "docker-compose.yml": None
            },
            "django-app": {
                "myproject": {
                    "settings": {
                        "__init__.py": None,
                        "base.py": None,
                        "development.py": None,
                        "production.py": None
                    },
                    "urls.py": None,
                    "wsgi.py": None,
                    "asgi.py": None,
                    "__init__.py": None
                },
                "apps": {
                    "users": {
                        "migrations": {},
                        "models.py": None,
                        "views.py": None,
                        "urls.py": None,
                        "serializers.py": None,
                        "tests.py": None,
                        "admin.py": None,
                        "__init__.py": None
                    },
                    "core": {
                        "management": {
                            "commands": {}
                        },
                        "utils.py": None,
                        "__init__.py": None
                    }
                },
                "static": {
                    "css": {},
                    "js": {},
                    "images": {}
                },
                "media": {},
                "templates": {
                    "base.html": None,
                    "components": {}
                },
                "tests": {
                    "unit": {},
                    "integration": {}
                },
                "docs": {
                    "api.md": None
                },
                "scripts": {
                    "deploy.sh": None,
                    "backup.sh": None
                },
                "locale": {},
                "venv": {},
                ".gitignore": None,
                "requirements.txt": None,
                "requirements-dev.txt": None,
                "README.md": None,
                "manage.py": None,
                ".env": None,
                ".env.example": None,
                "Dockerfile": None,
                "docker-compose.yml": None,
                "pytest.ini": None
            },
            "fastapi-app": {
                "app": {
                    "api": {
                        "v1": {
                            "endpoints": {},
                            "__init__.py": None
                        },
                        "__init__.py": None
                    },
                    "core": {
                        "config.py": None,
                        "security.py": None,
                        "dependencies.py": None,
                        "__init__.py": None
                    },
                    "models": {
                        "__init__.py": None
                    },
                    "schemas": {
                        "__init__.py": None
                    },
                    "services": {
                        "__init__.py": None
                    },
                    "utils": {
                        "__init__.py": None
                    },
                    "main.py": None,
                    "__init__.py": None
                },
                "tests": {
                    "unit": {},
                    "integration": {},
                    "conftest.py": None
                },
                "migrations": {
                    "versions": {}
                },
                "scripts": {
                    "start.sh": None
                },
                "docs": {
                    "openapi.json": None
                },
                ".gitignore": None,
                "requirements.txt": None,
                "requirements-dev.txt": None,
                "README.md": None,
                ".env": None,
                "Dockerfile": None,
                "docker-compose.yml": None,
                "pyproject.toml": None
            },
            "vue-app": {
                "public": {
                    "index.html": None,
                    "favicon.ico": None
                },
                "src": {
                    "assets": {
                        "images": {},
                        "styles": {}
                    },
                    "components": {
                        "common": {},
                        "layout": {}
                    },
                    "views": {},
                    "router": {
                        "index.js": None
                    },
                    "store": {
                        "modules": {},
                        "index.js": None
                    },
                    "composables": {},
                    "utils": {},
                    "services": {
                        "api.js": None
                    },
                    "plugins": {},
                    "App.vue": None,
                    "main.js": None
                },
                "tests": {
                    "unit": {},
                    "e2e": {}
                },
                "docs": {},
                "node_modules": {},
                "dist": {},
                ".gitignore": None,
                "package.json": None,
                "README.md": None,
                "vue.config.js": None,
                "babel.config.js": None,
                "jest.config.js": None,
                ".env": None
            },
            "data-science-project": {
                "data": {
                    "raw": {},
                    "processed": {},
                    "external": {},
                    "interim": {}
                },
                "notebooks": {
                    "exploratory": {},
                    "modeling": {}
                },
                "src": {
                    "data": {
                        "make_dataset.py": None
                    },
                    "features": {
                        "build_features.py": None
                    },
                    "models": {
                        "train_model.py": None,
                        "predict_model.py": None
                    },
                    "visualization": {
                        "visualize.py": None
                    },
                    "utils": {
                        "helpers.py": None
                    }
                },
                "tests": {
                    "test_data.py": None,
                    "test_models.py": None
                },
                "models": {
                    "trained": {},
                    "experiments": {}
                },
                "reports": {
                    "figures": {}
                },
                "config": {
                    "config.yaml": None
                },
                "scripts": {
                    "preprocess.py": None,
                    "train.py": None
                },
                "docs": {
                    "report.md": None,
                    "methodology.md": None
                },
                "environment": {},
                ".gitignore": None,
                "requirements.txt": None,
                "README.md": None,
                ".env": None,
                "setup.py": None,
                "Makefile": None
            },
            "flutter-app": {
                "android": {},
                "ios": {},
                "lib": {
                    "models": {},
                    "screens": {
                        "auth": {},
                        "main": {}
                    },
                    "widgets": {
                        "common": {}
                    },
                    "services": {
                        "api": {},
                        "local_storage": {}
                    },
                    "utils": {
                        "constants.dart": None,
                        "helpers.dart": None
                    },
                    "providers": {},
                    "routes": {
                        "app_router.dart": None
                    },
                    "theme": {
                        "app_theme.dart": None
                    },
                    "main.dart": None
                },
                "assets": {
                    "images": {
                        "icons": {}
                    },
                    "fonts": {}
                },
                "test": {
                    "widget_test": {},
                    "unit_test": {}
                },
                "integration_test": {},
                "docs": {
                    "setup.md": None
                },
                ".gitignore": None,
                "pubspec.yaml": None,
                "README.md": None,
                "analysis_options.yaml": None
            },
            "go-microservice": {
                "cmd": {
                    "api": {
                        "main.go": None
                    },
                    "worker": {
                        "main.go": None
                    }
                },
                "internal": {
                    "api": {
                        "handlers": {},
                        "middleware": {},
                        "routes": {}
                    },
                    "config": {
                        "config.go": None
                    },
                    "database": {
                        "migrations": {},
                        "seeds": {}
                    },
                    "models": {},
                    "services": {},
                    "utils": {}
                },
                "pkg": {
                    "logger": {},
                    "validator": {},
                    "response": {}
                },
                "api": {
                    "swagger": {
                        "docs.go": None
                    }
                },
                "tests": {
                    "unit": {},
                    "integration": {},
                    "mocks": {}
                },
                "deployments": {
                    "docker": {},
                    "k8s": {}
                },
                "scripts": {
                    "build.sh": None,
                    "test.sh": None
                },
                "docs": {
                    "api.md": None
                },
                ".gitignore": None,
                "go.mod": None,
                "go.sum": None,
                "README.md": None,
                "Dockerfile": None,
                "Makefile": None
            },
            "mobile-app-rn": {
                "android": {},
                "ios": {},
                "src": {
                    "components": {
                        "common": {},
                        "forms": {}
                    },
                    "screens": {
                        "auth": {},
                        "main": {},
                        "profile": {}
                    },
                    "navigation": {
                        "AppNavigator.js": None,
                        "AuthNavigator.js": None
                    },
                    "services": {
                        "api": {},
                        "storage": {},
                        "notifications": {}
                    },
                    "utils": {
                        "constants.js": None,
                        "helpers.js": None
                    },
                    "hooks": {},
                    "context": {},
                    "assets": {
                        "images": {},
                        "fonts": {}
                    },
                    "styles": {
                        "colors.js": None,
                        "typography.js": None
                    }
                },
                "tests": {
                    "__tests__": {},
                    "e2e": {}
                },
                "scripts": {
                    "build-android.sh": None,
                    "build-ios.sh": None
                },
                "docs": {
                    "setup.md": None
                },
                "node_modules": {},
                ".gitignore": None,
                "package.json": None,
                "README.md": None,
                ".env": None,
                "metro.config.js": None,
                "app.json": None,
                "babel.config.js": None
            }
        }
        if os.path.exists(self.presets_file):
            try:
                with open(self.presets_file, 'r') as f:
                    loaded_presets = json.load(f)
                default_presets.update(loaded_presets)
                return default_presets
            except json.JSONDecodeError:
                return default_presets
        return default_presets

    def save_presets(self):
        """Save presets to JSON file."""
        try:
            with open(self.presets_file, 'w') as f:
                json.dump(self.presets, f, indent=2)
        except Exception as e:
            print(f"Error saving presets: {str(e)}")

    def create_structure(self, base_path, structure):
        """Create folder structure recursively."""
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if content is None:  # File
                with open(path, 'w') as f:
                    f.write("")  # Create empty file
            else:  # Directory
                os.makedirs(path, exist_ok=True)
                self.create_structure(path, content)

    def create_project(self, preset_name, project_path):
        """Create project structure from preset."""
        if preset_name in self.presets:
            self.create_structure(project_path, self.presets[preset_name])
            return True
        return False
    
    def create_project_with_progress(self, preset_name, project_path, progress_callback):
        """Create project structure with progress updates."""
        if preset_name not in self.presets:
            return False
        
        structure = self.presets[preset_name]
        total_items = self._count_items(structure)
        created_items = 0
        
        def create_with_progress(base_path, structure_dict):
            nonlocal created_items
            for name, content in structure_dict.items():
                item_path = os.path.join(base_path, name)
                if content is None:  # File
                    with open(item_path, 'w') as f:
                        f.write('')
                else:  # Directory
                    os.makedirs(item_path, exist_ok=True)
                    if content:
                        create_with_progress(item_path, content)
                
                created_items += 1
                progress = int(30 + (created_items / total_items) * 60)
                progress_callback.emit(progress, f"Created: {name}")
                time.sleep(0.05)  # Small delay for visual feedback
        
        try:
            os.makedirs(project_path, exist_ok=True)
            create_with_progress(project_path, structure)
            return True
        except Exception:
            return False
    
    def _count_items(self, structure):
        """Count total number of items in structure for progress calculation."""
        count = 0
        for name, content in structure.items():
            count += 1
            if content and isinstance(content, dict):
                count += self._count_items(content)
        return count

    def add_preset(self, preset_name, structure):
        """Add a new preset and save to file."""
        self.presets[preset_name] = structure
        self.save_presets()

    def delete_preset(self, preset_name):
        """Delete a preset."""
        if preset_name in self.presets:
            del self.presets[preset_name]
            self.save_presets()
            return True
        return False

    def tree_to_structure(self, tree):
        """Convert QTreeWidget to structure dictionary."""
        structure = {}
        root = tree.topLevelItem(0)
        if not root:
            return structure
        def build_structure(item):
            name = item.text(0)[2:].strip()  # Remove icon
            children = [item.child(i) for i in range(item.childCount())]
            if item.text(0).startswith("📁"):
                result = {}
                for child in children:
                    result.update(build_structure(child))
                return {name: result}
            return {name: None}
        for i in range(root.childCount()):
            structure.update(build_structure(root.child(i)))
        return structure

class PresetEditorWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Custom Preset Builder")
        self.setGeometry(150, 150, 1000, 700)
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f0f23, stop:1 #1a1a2e);
            }
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: 500;
            }
            QLineEdit {
                background-color: #16213e;
                color: #e0e0e0;
                border: 2px solid #0e3460;
                border-radius: 10px;
                padding: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
                background-color: #1a2751;
            }
            QTreeWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #16213e, stop:1 #0e1b2e);
                color: #e0e0e0;
                border: 2px solid #0e3460;
                border-radius: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                selection-background-color: #4a90e2;
                outline: none;
            }
            QTreeWidget::item {
                padding: 8px;
                border-radius: 6px;
                margin: 2px;
            }
            QTreeWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2, stop:1 #357abd);
                color: white;
            }
            QTreeWidget::item:hover {
                background-color: #2a3f5f;
            }
            QMenu {
                background-color: #1a2751;
                color: #e0e0e0;
                border: 1px solid #4a90e2;
                border-radius: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 6px;
            }
            QMenu::item:selected {
                background-color: #4a90e2;
                color: white;
            }
            QGroupBox {
                color: #e0e0e0;
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #0e3460;
                border-radius: 10px;
                margin: 10px 0;
                padding-top: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Left panel for controls
        left_panel = QWidget()
        left_panel.setMaximumWidth(350)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(20)

        # Title
        title = QLabel("🏗️ Preset Builder")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4a90e2;
            padding: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(74, 144, 226, 0.1), stop:1 rgba(74, 144, 226, 0.05));
            border-radius: 12px;
        """)
        left_layout.addWidget(title)

        # Preset name group
        name_group = QGroupBox("Preset Information")
        name_layout = QVBoxLayout(name_group)
        name_layout.addWidget(QLabel("Preset Name:"))
        self.preset_name = QLineEdit()
        self.preset_name.setPlaceholderText("Enter a descriptive name for your preset")
        name_layout.addWidget(self.preset_name)
        name_layout.addWidget(QLabel("Description (optional):"))
        self.preset_description = QLineEdit()
        self.preset_description.setPlaceholderText("Brief description of this project structure")
        name_layout.addWidget(self.preset_description)
        left_layout.addWidget(name_group)

        # Instructions
        instructions = QLabel("""
📝 Instructions:
• Right-click in the structure tree to add folders/files
• Drag and drop to reorganize items
• This is a simulation - no actual files are created
• Click 'Save Preset' to store your custom structure
        """)
        instructions.setStyleSheet("""
            background-color: rgba(74, 144, 226, 0.1);
            padding: 15px;
            border-radius: 10px;
            color: #b0b0b0;
            font-size: 13px;
            line-height: 1.4;
        """)
        instructions.setWordWrap(True)
        left_layout.addWidget(instructions)

        # Save button
        self.save_button = AnimatedButton("💾 Save Preset")
        self.save_button.clicked.connect(self.save_preset)
        left_layout.addWidget(self.save_button)
        left_layout.addStretch()
        main_layout.addWidget(left_panel)

        # Right panel for tree
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        tree_label = QLabel("📂 Project Structure Preview")
        tree_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4a90e2; padding: 10px 0;")
        right_layout.addWidget(tree_label)

        # Tree widget with drag-and-drop enabled
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDropIndicatorShown(True)
        self.tree.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.tree.setAnimated(True)
        right_layout.addWidget(self.tree)

        # Context menu
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)

        # Create root item
        root = QTreeWidgetItem(self.tree, ["📁 Project Root"])
        root.setFlags(root.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsDropEnabled)
        root.setExpanded(True)
        main_layout.addWidget(right_panel, 2)

    def show_context_menu(self, pos):
        item = self.tree.itemAt(pos)
        menu = QMenu(self)
        menu.addAction("📁 Add Folder", lambda: self.add_item(item, True))
        menu.addAction("📄 Add File", lambda: self.add_item(item, False))
        if item and item.text(0) != "📁 Project Root":
            menu.addSeparator()
            menu.addAction("✏️ Rename", lambda: self.rename_item(item))
            menu.addAction("🗑️ Delete", lambda: self.delete_item(item))
        menu.exec(self.tree.mapToGlobal(pos))

    def add_item(self, parent, is_folder):
        if not parent:
            parent = self.tree.topLevelItem(0)
        if parent and parent.text(0).startswith("📄"):
            QMessageBox.warning(self, "Invalid Operation", "Cannot add items inside a file!")
            return
        item_type = "folder" if is_folder else "file"
        name, ok = QInputDialog.getText(
            self,
            f"New {item_type.title()}",
            f"Enter {item_type} name:",
            text=f"new_{item_type}"
        )
        if not ok or not name.strip():
            return
        icon = "📁" if is_folder else "📄"
        item = QTreeWidgetItem(parent, [f"{icon} {name.strip()}"])
        if is_folder:
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsDropEnabled)
        parent.setExpanded(True)
        self.tree.setCurrentItem(item)

    def rename_item(self, item):
        if not item or item.text(0) == "📁 Project Root":
            return
        self.tree.editItem(item, 0)

    def delete_item(self, item):
        if item and item.text(0) != "📁 Project Root":
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete '{item.text(0)}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                parent = item.parent()
                if parent:
                    parent.removeChild(item)

    def save_preset(self):
        name = self.preset_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing Information", "Please provide a preset name!")
            return
        structure = self.parent().creator.tree_to_structure(self.tree)
        if not structure:
            QMessageBox.warning(self, "Empty Structure", "Please add some folders or files to your structure!")
            return
        if name in self.parent().creator.presets:
            reply = QMessageBox.question(
                self,
                "Preset Exists",
                f"A preset named '{name}' already exists. Do you want to overwrite it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        self.parent().creator.add_preset(name, structure)
        self.parent().refresh_presets()
        QMessageBox.information(
            self,
            "Success! 🎉",
            f"Preset '{name}' has been saved successfully!"
        )
        self.close()

class PresetManagerWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Preset Manager")
        self.setGeometry(200, 200, 800, 600)
        self.setup_styles()
        self.setup_ui()
        self.refresh_presets()

    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f0f23, stop:1 #1a1a2e);
            }
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QListWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #16213e, stop:1 #0e1b2e);
                color: #e0e0e0;
                border: 2px solid #0e3460;
                border-radius: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 8px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2, stop:1 #357abd);
            }
            QListWidget::item:hover {
                background-color: #2a3f5f;
            }
            QTextEdit {
                background-color: #16213e;
                color: #e0e0e0;
                border: 2px solid #0e3460;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Left panel - preset list
        left_panel = QWidget()
        left_panel.setMaximumWidth(300)
        left_layout = QVBoxLayout(left_panel)
        title = QLabel("📋 Available Presets")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4a90e2; padding: 10px 0;")
        left_layout.addWidget(title)
        self.preset_list = QListWidget()
        left_layout.addWidget(self.preset_list)

        # Buttons
        button_layout = QHBoxLayout()
        self.delete_btn = AnimatedButton("🗑️ Delete")
        self.delete_btn.clicked.connect(self.delete_preset)
        self.delete_btn.setEnabled(False)
        button_layout.addWidget(self.delete_btn)
        self.export_btn = AnimatedButton("📤 Export")
        self.export_btn.clicked.connect(self.export_preset)
        self.export_btn.setEnabled(False)
        button_layout.addWidget(self.export_btn)
        left_layout.addLayout(button_layout)
        layout.addWidget(left_panel)

        # Right panel - preset preview
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        preview_title = QLabel("👁️ Preset Preview")
        preview_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4a90e2; padding: 10px 0;")
        right_layout.addWidget(preview_title)
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setPlaceholderText("Select a preset to see its structure...")
        right_layout.addWidget(self.preview_text)
        layout.addWidget(right_panel)

        # Connect selection change
        self.preset_list.currentItemChanged.connect(self.on_preset_selected)

    def refresh_presets(self):
        self.preset_list.clear()
        for preset_name in self.parent().creator.presets.keys():
            self.preset_list.addItem(f"📁 {preset_name}")

    def on_preset_selected(self, current, previous):
        if current:
            preset_name = current.text()[2:]  # Remove emoji
            self.delete_btn.setEnabled(True)
            self.export_btn.setEnabled(True)
            self.show_preset_preview(preset_name)
        else:
            self.delete_btn.setEnabled(False)
            self.export_btn.setEnabled(False)
            self.preview_text.clear()

    def show_preset_preview(self, preset_name):
        if preset_name in self.parent().creator.presets:
            structure = self.parent().creator.presets[preset_name]
            preview = self.format_structure(structure)
            self.preview_text.setPlainText(preview)

    def format_structure(self, structure, indent=0):
        result = []
        for name, content in structure.items():
            prefix = " " * indent
            if content is None:  # File
                result.append(f"{prefix}📄 {name}")
            else:  # Directory
                result.append(f"{prefix}📁 {name}/")
                if content:
                    result.append(self.format_structure(content, indent + 1))
        return "\n".join(result)

    def delete_preset(self):
        current_item = self.preset_list.currentItem()
        if current_item:
            preset_name = current_item.text()[2:]
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete the preset '{preset_name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.parent().creator.delete_preset(preset_name)
                self.parent().refresh_presets()
                self.refresh_presets()
                QMessageBox.information(self, "Success", f"Preset '{preset_name}' deleted successfully!")

    def export_preset(self):
        current_item = self.preset_list.currentItem()
        if current_item:
            preset_name = current_item.text()[2:]
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Preset",
                f"{preset_name}.json",
                "JSON Files (*.json)"
            )
            if file_path:
                try:
                    preset_data = {preset_name: self.parent().creator.presets[preset_name]}
                    with open(file_path, 'w') as f:
                        json.dump(preset_data, f, indent=2)
                    QMessageBox.information(self, "Success", f"Preset exported to {file_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to export preset: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blueprint Generator")
        self.setGeometry(100, 100, 1200, 800)
        self.setAcceptDrops(True)  # Enable drag & drop
        
        # Initialize components
        self.creator = ProjectStructureCreator()
        self.settings = QSettings('ProjectCreatorPro', 'Settings')
        self.recent_projects = self.load_recent_projects()
        self.creation_thread = None
        
        # Setup UI and features
        self.setup_styles()
        self.setup_ui()
        self.setup_keyboard_shortcuts()
        self.setup_status_bar()
        self.load_user_preferences()
        
        # Auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.save_user_preferences)
        self.auto_save_timer.start(30000)  # Save every 30 seconds

    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f0f23, stop:1 #1a1a2e);
            }
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: 500;
            }
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a3f5f, stop:1 #1a2f4f);
                color: #e0e0e0;
                border: 2px solid #0e3460;
                border-radius: 10px;
                padding: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                min-width: 200px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #4a90e2;
                margin-right: 10px;
            }
            QComboBox:hover {
                border-color: #4a90e2;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a4f6f, stop:1 #2a3f5f);
            }
            QComboBox QAbstractItemView {
                background-color: #1a2751;
                color: #e0e0e0;
                selection-background-color: #4a90e2;
                border: 1px solid #4a90e2;
                border-radius: 8px;
            }
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #16213e, stop:1 #0e1b2e);
                color: #e0e0e0;
                border: 2px solid #0e3460;
                border-radius: 10px;
                padding: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a2751, stop:1 #16213e);
            }
            QGroupBox {
                color: #e0e0e0;
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #0e3460;
                border-radius: 12px;
                margin: 15px 0;
                padding-top: 25px;
                background: rgba(22, 33, 62, 0.3);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                color: #4a90e2;
            }
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #16213e, stop:1 #0e1b2e);
                color: #e0e0e0;
                border: 2px solid #0e3460;
                border-radius: 10px;
                padding: 15px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                line-height: 1.4;
            }
        """)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("🚀 Blueprint Generator")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #4a90e2;
            padding: 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(74, 144, 226, 0.15), stop:1 rgba(74, 144, 226, 0.05));
            border-radius: 15px;
            border: 1px solid rgba(74, 144, 226, 0.3);
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        version = QLabel("v2.0")
        version.setStyleSheet("font-size: 14px; color: #888; padding: 10px;")
        header_layout.addWidget(version)
        main_layout.addLayout(header_layout)

        # Content area with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Left panel - Controls
        left_panel = QWidget()
        left_panel.setMaximumWidth(450)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(20)

        # Preset selection group
        preset_group = QGroupBox("📁 Project Template")
        preset_layout = QVBoxLayout(preset_group)
        preset_layout.addWidget(QLabel("Choose a template:"))
        self.preset_combo = QComboBox()
        self.preset_combo.currentTextChanged.connect(self.on_preset_changed)
        preset_layout.addWidget(self.preset_combo)
        self.template_description = QTextEdit()
        self.template_description.setMaximumHeight(100)
        self.template_description.setPlaceholderText("Template description will appear here...")
        self.template_description.setReadOnly(True)
        preset_layout.addWidget(QLabel("Description:"))
        preset_layout.addWidget(self.template_description)
        left_layout.addWidget(preset_group)

        # Path selection group
        path_group = QGroupBox("📂 Destination")
        path_layout = QVBoxLayout(path_group)
        path_layout.addWidget(QLabel("Select where to create your project (or drag & drop):"))
        path_input_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Choose destination folder or drag & drop here...")
        self.path_input.textChanged.connect(self.validate_input)
        self.path_input.setToolTip("Enter the destination path or drag a folder here")
        path_input_layout.addWidget(self.path_input)
        browse_button = AnimatedButton("🔍 Browse", tooltip="Browse for destination folder (Ctrl+B)")
        browse_button.clicked.connect(self.browse_path)
        path_input_layout.addWidget(browse_button)
        path_layout.addLayout(path_input_layout)
        
        # Path validation indicator
        self.path_status = QLabel("")
        self.path_status.setStyleSheet("color: #888; font-size: 12px; padding: 5px;")
        path_layout.addWidget(self.path_status)
        left_layout.addWidget(path_group)

        # Action buttons
        button_group = QGroupBox("⚡ Actions")
        button_layout = QVBoxLayout(button_group)
        self.create_button = AnimatedButton("🎯 Create Project Structure", tooltip="Create project structure (Ctrl+Enter)")
        self.create_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 24px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #239b56, stop:1 #1e8449);
            }
        """)
        self.create_button.clicked.connect(self.create_project)
        button_layout.addWidget(self.create_button)
        
        # Recent projects button
        recent_button = AnimatedButton("📋 Recent Projects", tooltip="Quick access to recent projects (Ctrl+R)")
        recent_button.clicked.connect(self.show_recent_projects)
        button_layout.addWidget(recent_button)
        
        secondary_layout = QHBoxLayout()
        new_preset_button = AnimatedButton("➕ New", tooltip="Create new preset (Ctrl+N)")
        new_preset_button.clicked.connect(self.open_preset_editor)
        secondary_layout.addWidget(new_preset_button)
        manage_button = AnimatedButton("⚙️ Manage", tooltip="Manage presets (Ctrl+M)")
        manage_button.clicked.connect(self.open_preset_manager)
        secondary_layout.addWidget(manage_button)
        import_button = AnimatedButton("📥 Import", tooltip="Import presets (Ctrl+I)")
        import_button.clicked.connect(self.import_preset)
        secondary_layout.addWidget(import_button)
        button_layout.addLayout(secondary_layout)
        left_layout.addWidget(button_group)
        left_layout.addStretch()
        splitter.addWidget(left_panel)

        # Right panel - Preview
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        preview_title = QLabel("👁️ Structure Preview")
        preview_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4a90e2; padding: 10px 0;")
        right_layout.addWidget(preview_title)
        self.preview_area = QTextEdit()
        self.preview_area.setReadOnly(True)
        self.preview_area.setPlaceholderText("Select a template to see the project structure preview...")
        right_layout.addWidget(self.preview_area)
        splitter.addWidget(right_panel)
        splitter.setSizes([450, 750])

        # Progress bar (initially hidden)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #0e3460;
                border-radius: 8px;
                text-align: center;
                background: #16213e;
                color: #e0e0e0;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
                border-radius: 6px;
            }
        """)
        main_layout.addWidget(self.progress_bar)
        
        # Initialize
        self.refresh_presets()
        self.update_recent_projects_menu()

    def refresh_presets(self):
        current = self.preset_combo.currentText()
        self.preset_combo.clear()
        presets = list(self.creator.presets.keys())
        self.preset_combo.addItems(presets)
        if current and current in presets:
            self.preset_combo.setCurrentText(current)
        elif presets:
            self.preset_combo.setCurrentIndex(0)

    def on_preset_changed(self, preset_name):
        if preset_name and preset_name in self.creator.presets:
            structure = self.creator.presets[preset_name]
            preview = self.format_structure_preview(structure)
            self.preview_area.setPlainText(preview)
            descriptions = {
                "react-app": "Modern React application with TypeScript support, testing setup, and build tools.",
                "nextjs-app": "Next.js application with app router, TypeScript, and Tailwind CSS setup.",
                "express-api": "Express.js REST API with middleware, authentication, and database integration.",
                "django-app": "Django web application with apps structure, settings management, and deployment files.",
                "fastapi-app": "FastAPI application with async support, automatic API documentation, and testing.",
                "vue-app": "Vue.js application with router, state management, and component structure.",
                "data-science-project": "Data science project with notebooks, data pipelines, and model organization.",
                "flutter-app": "Flutter mobile application with proper architecture and platform-specific code.",
                "go-microservice": "Go microservice with clean architecture, API documentation, and deployment files.",
                "mobile-app-rn": "React Native mobile app with navigation, services, and cross-platform support."
            }
            description = descriptions.get(preset_name, "Custom project template structure.")
            self.template_description.setPlainText(description)

    def format_structure_preview(self, structure, indent=0):
        result = []
        for name, content in structure.items():
            prefix = " " * indent
            if content is None:  # File
                result.append(f"{prefix}📄 {name}")
            else:  # Directory
                result.append(f"{prefix}📁 {name}/")
                if content:
                    result.append(self.format_structure_preview(content, indent + 1))
        return "\n".join(result)

    def browse_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if path:
            self.path_input.setText(path)

    def create_project(self):
        preset_name = self.preset_combo.currentText()
        project_path = self.path_input.text().strip()
        
        # Enhanced validation
        if not preset_name:
            self.show_status_message("Please select a project template!", error=True)
            QMessageBox.warning(self, "No Template Selected", "Please select a project template!")
            return
        if not project_path:
            self.show_status_message("Please select a destination folder!", error=True)
            QMessageBox.warning(self, "No Destination", "Please select a destination folder!")
            return
        
        # Check if path is valid
        try:
            os.path.abspath(project_path)
        except Exception:
            self.show_status_message("Invalid path format!", error=True)
            QMessageBox.warning(self, "Invalid Path", "Please enter a valid path!")
            return
        
        if not os.path.exists(project_path):
            reply = QMessageBox.question(
                self,
                "Create Directory",
                f"The directory '{project_path}' doesn't exist. Create it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        # Start project creation with progress feedback
        self.create_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.show_status_message("Creating project structure...")
        
        # Create project in background thread
        self.creation_thread = ProjectCreationThread(self.creator, preset_name, project_path)
        self.creation_thread.progress_updated.connect(self.update_progress)
        self.creation_thread.creation_finished.connect(self.on_creation_finished)
        self.creation_thread.start()
    
    def update_progress(self, value, message):
        """Update progress bar and status message."""
        self.progress_bar.setValue(value)
        self.show_status_message(message)
    
    def on_creation_finished(self, success, message):
        """Handle project creation completion."""
        self.progress_bar.setVisible(False)
        self.create_button.setEnabled(True)
        
        if success:
            project_path = self.path_input.text().strip()
            self.add_to_recent_projects(project_path)
            self.show_status_message("Project created successfully!", success=True)
            
            # Success message with options
            msg = QMessageBox(self)
            msg.setWindowTitle("Success! 🎉")
            msg.setText(f"Project structure created successfully at:\n{project_path}")
            msg.setInformativeText("What would you like to do next?")
            open_folder_btn = msg.addButton("📁 Open Folder", QMessageBox.ButtonRole.ActionRole)
            create_another_btn = msg.addButton("🔄 Create Another", QMessageBox.ButtonRole.ActionRole)
            msg.addButton(QMessageBox.StandardButton.Ok)
            
            msg.exec()
            
            if msg.clickedButton() == open_folder_btn:
                self.open_project_folder(project_path)
            elif msg.clickedButton() == create_another_btn:
                self.path_input.clear()
                self.preset_combo.setCurrentIndex(0)
        else:
            self.show_status_message("Failed to create project!", error=True)
            QMessageBox.critical(self, "Error", message)

    def open_preset_editor(self):
        self.preset_editor = PresetEditorWindow(self)
        self.preset_editor.show()

    def open_preset_manager(self):
        self.preset_manager = PresetManagerWindow(self)
        self.preset_manager.show()

    def import_preset(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Preset",
            "",
            "JSON Files (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    preset_data = json.load(f)
                imported_count = 0
                for name, structure in preset_data.items():
                    if name in self.creator.presets:
                        reply = QMessageBox.question(
                            self,
                            "Preset Exists",
                            f"Preset '{name}' already exists. Overwrite?",
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                        )
                        if reply != QMessageBox.StandardButton.Yes:
                            continue
                    self.creator.add_preset(name, structure)
                    imported_count += 1
                self.refresh_presets()
                QMessageBox.information(
                    self,
                    "Import Complete",
                    f"Successfully imported {imported_count} preset(s)!"
                )
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Failed to import preset:\n{str(e)}")
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for better UX."""
        # Create project shortcut
        create_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        create_shortcut.activated.connect(self.create_project)
        
        # Browse shortcut
        browse_shortcut = QShortcut(QKeySequence("Ctrl+B"), self)
        browse_shortcut.activated.connect(self.browse_path)
        
        # New preset shortcut
        new_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        new_shortcut.activated.connect(self.open_preset_editor)
        
        # Manage presets shortcut
        manage_shortcut = QShortcut(QKeySequence("Ctrl+M"), self)
        manage_shortcut.activated.connect(self.open_preset_manager)
        
        # Import shortcut
        import_shortcut = QShortcut(QKeySequence("Ctrl+I"), self)
        import_shortcut.activated.connect(self.import_preset)
        
        # Recent projects shortcut
        recent_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        recent_shortcut.activated.connect(self.show_recent_projects)
        
        # Quit shortcut
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self.close)
    
    def setup_status_bar(self):
        """Setup status bar for feedback."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: #16213e;
                color: #e0e0e0;
                border-top: 1px solid #0e3460;
                padding: 5px;
            }
        """)
        self.show_status_message("Ready to create project structures")
    
    def show_status_message(self, message, timeout=3000, success=False, error=False):
        """Show status message with optional styling."""
        if success:
            self.status_bar.setStyleSheet("""
                QStatusBar {
                    background: #27ae60;
                    color: white;
                    border-top: 1px solid #229954;
                    padding: 5px;
                }
            """)
        elif error:
            self.status_bar.setStyleSheet("""
                QStatusBar {
                    background: #e74c3c;
                    color: white;
                    border-top: 1px solid #c0392b;
                    padding: 5px;
                }
            """)
        else:
            self.status_bar.setStyleSheet("""
                QStatusBar {
                    background: #16213e;
                    color: #e0e0e0;
                    border-top: 1px solid #0e3460;
                    padding: 5px;
                }
            """)
        
        self.status_bar.showMessage(message, timeout)
        
        # Reset style after timeout
        if success or error:
            QTimer.singleShot(timeout, lambda: self.status_bar.setStyleSheet("""
                QStatusBar {
                    background: #16213e;
                    color: #e0e0e0;
                    border-top: 1px solid #0e3460;
                    padding: 5px;
                }
            """))
    
    def validate_input(self):
        """Validate path input in real-time."""
        path = self.path_input.text().strip()
        if not path:
            self.path_status.setText("")
            self.create_button.setEnabled(True)
            return
        
        try:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                if os.path.isdir(abs_path):
                    self.path_status.setText("✓ Valid directory")
                    self.path_status.setStyleSheet("color: #27ae60; font-size: 12px; padding: 5px;")
                    self.create_button.setEnabled(True)
                else:
                    self.path_status.setText("⚠ Path exists but is not a directory")
                    self.path_status.setStyleSheet("color: #f39c12; font-size: 12px; padding: 5px;")
                    self.create_button.setEnabled(False)
            else:
                parent_dir = os.path.dirname(abs_path)
                if os.path.exists(parent_dir) and os.path.isdir(parent_dir):
                    self.path_status.setText("ℹ Directory will be created")
                    self.path_status.setStyleSheet("color: #3498db; font-size: 12px; padding: 5px;")
                    self.create_button.setEnabled(True)
                else:
                    self.path_status.setText("✗ Invalid path")
                    self.path_status.setStyleSheet("color: #e74c3c; font-size: 12px; padding: 5px;")
                    self.create_button.setEnabled(False)
        except Exception:
            self.path_status.setText("✗ Invalid path format")
            self.path_status.setStyleSheet("color: #e74c3c; font-size: 12px; padding: 5px;")
            self.create_button.setEnabled(False)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop events for folder paths."""
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if os.path.isdir(path):
                self.path_input.setText(path)
                self.show_status_message(f"Dropped folder: {os.path.basename(path)}")
            else:
                self.show_status_message("Please drop a folder, not a file", error=True)
    
    def load_recent_projects(self):
        """Load recent projects from settings."""
        return self.settings.value('recent_projects', [])
    
    def add_to_recent_projects(self, path):
        """Add project to recent projects list."""
        if path in self.recent_projects:
            self.recent_projects.remove(path)
        self.recent_projects.insert(0, path)
        self.recent_projects = self.recent_projects[:10]  # Keep only 10 recent
        self.settings.setValue('recent_projects', self.recent_projects)
        self.update_recent_projects_menu()
    
    def update_recent_projects_menu(self):
        """Update recent projects menu (placeholder for now)."""
        pass  # Could be expanded to show in a menu
    
    def show_recent_projects(self):
        """Show recent projects dialog."""
        if not self.recent_projects:
            QMessageBox.information(self, "Recent Projects", "No recent projects found.")
            return
        
        from PyQt6.QtWidgets import QDialog, QListWidget, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Recent Projects")
        dialog.setGeometry(200, 200, 500, 300)
        layout = QVBoxLayout(dialog)
        
        list_widget = QListWidget()
        for project in self.recent_projects:
            if os.path.exists(project):
                list_widget.addItem(f"📁 {project}")
            else:
                list_widget.addItem(f"⚠ {project} (not found)")
        
        layout.addWidget(QLabel("Select a recent project to open:"))
        layout.addWidget(list_widget)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            current_item = list_widget.currentItem()
            if current_item:
                path = current_item.text().replace("📁 ", "").replace("⚠ ", "").split(" (not found)")[0]
                if os.path.exists(path):
                    self.open_project_folder(path)
                else:
                    QMessageBox.warning(self, "Path Not Found", f"The path no longer exists:\n{path}")
    
    def open_project_folder(self, path):
        """Open project folder in system file manager."""
        try:
            import subprocess
            import platform
            
            system = platform.system()
            if system == "Windows":
                subprocess.run(["explorer", path])
            elif system == "Darwin":  # macOS
                subprocess.run(["open", path])
            else:  # Linux and others
                subprocess.run(["xdg-open", path])
            
            self.show_status_message(f"Opened folder: {os.path.basename(path)}")
        except Exception as e:
            self.show_status_message(f"Failed to open folder: {str(e)}", error=True)
    
    def load_user_preferences(self):
        """Load user preferences from settings."""
        # Restore window geometry
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        
        # Restore last selected preset
        last_preset = self.settings.value('last_preset')
        if last_preset:
            index = self.preset_combo.findText(last_preset)
            if index >= 0:
                self.preset_combo.setCurrentIndex(index)
        
        # Restore last path
        last_path = self.settings.value('last_path')
        if last_path and os.path.exists(last_path):
            self.path_input.setText(last_path)
    
    def save_user_preferences(self):
        """Save user preferences to settings."""
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('last_preset', self.preset_combo.currentText())
        self.settings.setValue('last_path', os.path.dirname(self.path_input.text()) if self.path_input.text() else '')
    
    def closeEvent(self, event):
        """Handle application close event."""
        self.save_user_preferences()
        if self.creation_thread and self.creation_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "Project Creation in Progress",
                "A project is currently being created. Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
            self.creation_thread.terminate()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Blueprint Generator")
    app.setApplicationVersion("2.0")
    try:
        app.setWindowIcon(QIcon("icon.png"))
    except:
        pass
    window = MainWindow()
    window.show()
    sys.exit(app.exec())