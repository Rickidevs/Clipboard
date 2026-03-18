<div align="center">

```
⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⠙⢦⡀⠀⠀⣰⢶⠀⠀⠀
⠀⠀⠀⠀⠀⢻⠀⠀⠹⣦⠞⠁⢸⠀⠀⠀
⠀⠸⡟⠓⠒⠛⠀⡀⠤⠤⢀⠀⠾⠶⢶⡆
⠀⠀⢻⡀⠀⡐⠁⠀⠀⠀⠀⠑⡀⢀⡞⠀
⣀⡤⠞⠃⢰⠀⠐⠒⠲⡶⠶⠶⢶⠘⠲⣄
⠙⠲⣤⡀⢸⠀⡒⠖⠒⡲⡒⠒⢒⢢⡞⠉
⢀⡴⠋⠀⡸⠀⠌⠀⠈⢀⢉⠤⢽⡈⣳⡄
⠀⠙⢳⠆⠄⡀⠀⠀⠀⣀⣁⠀⢸⢾⡁⠀
⠀⠀⠙⠛⣷⣣⠠⠎⠀⣠⠔⠉⣼⠏⠁⠀
⠀⠀⠀⠀⠉⢉⣳⡤⠀⢀⣤⡞⠁⠀⠀⠀
⠀⠀⠀⡴⠋⠉⡑⠃⠒⠊⣌⠉⢳⡄⠀⠀
⠀⠀⠀⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠃⠀⠀
```

# Clipboard Manager

**A lightweight clipboard history tool for Linux — triggered by a global hotkey**

[![Python](https://img.shields.io/badge/Python-3.8%2B-FFD43B?style=flat-square&logo=python&logoColor=white&labelColor=306998)](https://python.org)
[![customtkinter](https://img.shields.io/badge/customtkinter-latest-blue?style=flat-square)](https://github.com/TomSchimansky/CustomTkinter)
[![Platform](https://img.shields.io/badge/Platform-Linux-orange?style=flat-square&logo=linux&logoColor=white)](/)
[![Stars](https://img.shields.io/github/stars/Rickidevs/Clipboard?style=flat-square&color=gold)](https://github.com/Rickidevs/Clipboard/stargazers)

[Overview](#overview) · [Features](#features) · [Installation](#installation) · [Usage](#usage) · [Configuration](#configuration) · [Service](#running-as-a-system-service)

</div>

---

## Overview

Clipboard Manager is a minimal background utility that tracks your clipboard history and surfaces it through a clean floating window — activated from anywhere on your desktop with `Ctrl + Alt + V`.

It runs silently as a background process (or a systemd service), monitors clipboard changes every 500ms, and stores up to 15 recent entries. Clicking any entry copies it back to the clipboard and closes the window.

---

## Features

- Global hotkey (`Ctrl + Alt + V`) to open the history window from any application
- Stores up to 15 unique clipboard entries, newest first
- Duplicate detection — re-copied text is moved to the top rather than duplicated
- Draggable floating window with no taskbar entry (`overrideredirect`)
- Scrollable entry list with single-click paste and auto-close
- Runs as a systemd service for automatic startup on login
- One-command setup script with automatic dependency installation

---

## Tech Stack

| Component | Library | Role |
|-----------|---------|------|
| GUI | customtkinter | Floating history window |
| Clipboard | pyperclip | Read & write clipboard content |
| Hotkey | keyboard | Global `Ctrl + Alt + V` listener |
| Threading | threading (stdlib) | Non-blocking clipboard monitor loop |
| Service | systemd | Auto-start on graphical login |

---

## Installation

### Requirements

- Linux (X11 display server)
- Python 3.8+
- `pip3`
- `sudo` access (for systemd service setup)

---

### Quick Setup

Clone the repository and run the setup script:

```bash
git clone https://github.com/Rickidevs/Clipboard.git
cd Clipboard
chmod +x setup.sh
./setup.sh
```

The script will:

1. Install any missing Python dependencies (`pyperclip`, `customtkinter`, `keyboard`)
2. Copy `Clipboard.py` to `/opt/Clipboard/`
3. Create and register a systemd service (`clipboard_monitor.service`)
4. Enable and start the service automatically

---

### Manual Dependency Install

If you prefer to install dependencies manually:

```bash
pip3 install pyperclip customtkinter keyboard
```

---

### Run Without Setup

To test the tool without installing the service:

```bash
python3 Clipboard.py
```

---

## Usage

Once the service is running (or the script is active), the tool works silently in the background.

| Action | Result |
|--------|--------|
| Copy anything (`Ctrl+C`) | Entry is added to history automatically |
| Press `Ctrl + Alt + V` | Opens the floating history window |
| Click an entry | Copies it to clipboard and closes the window |
| Press `Escape` | Closes the window |
| Drag the title bar | Repositions the window |

---

## Configuration

All visual and behavioral settings are defined as constants at the top of `Clipboard.py`:

```python
MAX_HISTORY     = 15          # Maximum number of entries to keep
WINDOW_WIDTH    = 380         # Floating window width (px)
WINDOW_HEIGHT   = 450         # Floating window height (px)
BACKGROUND_COLOR = "#1F1F1F"  # Window background
BUTTON_COLOR     = "#2B2B2B"  # Entry button color
BUTTON_HOVER     = "#3A3A3A"  # Entry button hover color
ACCENT_COLOR     = "#E0E0E0"  # Entry text color
HIGHLIGHT_COLOR  = "#00ADB5"  # Accent / highlight color
```

To change the hotkey, find this line in `Clipboard.py`:

```python
keyboard.add_hotkey('ctrl + alt + v', show_clipboard_history)
```

Replace `'ctrl + alt + v'` with any combination supported by the `keyboard` library, for example `'ctrl + shift + c'`.

---

## Running as a System Service

The setup script registers a `systemd` user service that starts automatically after the graphical session is ready.

### Service file location

```
/etc/systemd/system/clipboard_monitor.service
```

### Useful service commands

```bash
# Check current status
sudo systemctl status clipboard_monitor.service

# Stop the service
sudo systemctl stop clipboard_monitor.service

# Restart after making changes
sudo systemctl restart clipboard_monitor.service

# Disable autostart
sudo systemctl disable clipboard_monitor.service

# View logs
journalctl -u clipboard_monitor.service -f
```

> The service includes a 15-second startup delay (`ExecStartPre=/bin/sleep 15`) to ensure the display environment is fully initialized before the GUI launches.

---

## Project Structure

```
Clipboard/
├── Clipboard.py      # Main application — GUI, hotkey, clipboard monitor
└── setup.sh          # Automated install & systemd service registration
```

---

<div align="center">

**Built by [Rickidevs](https://github.com/Rickidevs)**

</div>
