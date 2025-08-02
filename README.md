# Blueprint Generator

A powerful and intuitive PyQt6-based GUI application for creating project folder structures from customizable templates. Perfect for developers who want to quickly scaffold new projects with consistent directory layouts.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## 🚀 Features

### Core Functionality
- **Template-Based Creation**: Choose from pre-built templates for popular frameworks (React, Next.js, Django, Flask, etc.)
- **Custom Templates**: Create and manage your own project structure templates
- **Instant Preview**: Visual preview of the folder structure before creation
- **Batch Operations**: Import/export multiple templates at once

### User Experience Enhancements
- **🎯 One-Click Creation**: Create entire project structures with a single click
- **📋 Recent Projects**: Quick access to recently created projects
- **🔍 Drag & Drop**: Drop folders directly into the path field
- **⌨️ Keyboard Shortcuts**: Power user shortcuts for all major actions
- **📊 Progress Feedback**: Real-time progress bar with status updates
- **✅ Input Validation**: Smart path validation with visual feedback
- **💾 Auto-Save**: Remembers your preferences and last used settings
- **🎨 Modern UI**: Beautiful dark theme with smooth animations


## 📸 Screenshots

### Main Interface
The clean, modern interface makes project creation intuitive and fast.
<img width="1199" height="1014" alt="image" src="https://github.com/user-attachments/assets/3801c24e-b6e4-4988-a2a5-5d9b848fb42b" />

### Template Builder
Create custom templates with the visual tree editor.

<img width="1000" height="744" alt="image" src="https://github.com/user-attachments/assets/02870353-d530-431a-ae49-5609342d7154" />

### Recent Projects
Quick access to your recently created projects.


## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- PyQt6

### Quick Install
```bash
# Clone the repository
git clone https://github.com/Sandelslover/Blueprint-generator.git
cd Blueprint-Generator

# Install dependencies
pip install PyQt6

# Run the application
python3 main.py
```


## 🎮 Usage

### Basic Usage
1. **Launch** the application
2. **Select** a project template from the dropdown
3. **Choose** or drag & drop your destination folder
4. **Click** "Create Project Structure" or press `Ctrl+Enter`
5. **Done!** Your project structure is ready

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Create project structure |
| `Ctrl+B` | Browse for destination folder |
| `Ctrl+N` | Create new template |
| `Ctrl+M` | Manage existing templates |
| `Ctrl+I` | Import templates |
| `Ctrl+R` | Show recent projects |
| `Ctrl+Q` | Quit application |

### Creating Custom Templates
1. Click **"➕ New"** or press `Ctrl+N`
2. Use the **Template Builder** to design your structure
3. **Right-click** to add folders and files
4. **Save** your template with a descriptive name
5. Your template is now available in the main dropdown

### Managing Templates
- **View**: See all your templates in the Template Manager
- **Edit**: Modify existing templates
- **Delete**: Remove templates you no longer need
- **Export**: Share templates with others
- **Import**: Load templates from other users

## 📁 Built-in Templates

The application comes with several pre-configured templates:

### Web Development
- **React App**: Modern React application structure
- **Next.js App**: Next.js 13+ app directory structure
- **Vue.js Project**: Vue 3 project layout
- **Angular App**: Angular CLI-style structure

### Backend Development
- **Django Project**: Full Django project with apps
- **Flask App**: Flask application structure
- **FastAPI Project**: Modern Python API structure
- **Node.js API**: Express.js API layout

### Mobile Development
- **React Native**: React Native project structure
- **Flutter App**: Flutter application layout

### General Purpose
- **Basic Web**: Simple HTML/CSS/JS structure
- **Documentation**: Documentation project layout
- **Python Package**: Python package structure

### Customizable Settings
- Window geometry and position
- Last selected template
- Recent projects list (up to 10)
- Default destination path



## 🐛 Troubleshooting

### Common Issues

**Application won't start**
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check PyQt6 installation
python3 -c "import PyQt6; print('PyQt6 installed successfully')"
```

**Templates not saving**
- Check write permissions in the application directory
- Ensure the `presets.json` file isn't read-only

**Drag & drop not working**
- This feature requires a desktop environment
- Try using the Browse button instead

### Getting Help
- Check the [Issues](https://github.com/Sandelslover/Blueprint-Generator/issues) page
- Create a new issue with detailed information
- Include your OS, Python version, and error messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for developers who value organized project structures**

