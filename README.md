# Clipboard Manager for Linux 📝🖥️

A simple and efficient clipboard manager for Linux users, inspired by Windows clipboard history. With just `CTRL + ALT + V`, access your clipboard's last 10 copied texts, and easily paste the one you need!

---

## Features ✨
- 🖱️ **Quick Access**: Show clipboard history with `CTRL + ALT + V`.
- 🔄 **Customizable**: Modify hotkey, window size, and other settings as per your needs.
- 🖥️ **Open-Source**: Feel free to tweak the code as it's open for all.
- 💻 **Lightweight**: A simple Python-based solution for your clipboard needs.

---

## Installation 🚀

Follow these steps to install the clipboard manager:

```bash
git clone https://github.com/Rickidevs/Clipboard.git
cd Clipboard
chmod +x setup.sh
./setup.sh
```

## Usage 🎮
Simply press `CTRL + ALT + V` to open the clipboard history window. Select the text you want to paste, and you're good to go!

### Customization Options 🎛️

If you want to customize some settings, make changes directly in the Clipboard.py file before running the setup.sh script:

🔑 **Shortcut Key:** Modify the hotkey at line 72. The default is `CTRL + ALT + V`, but you can change it to any other combination. The `WIN` key can sometimes cause issues on Linux, so adjust as needed.

🪟 **Window Size:** You can change the window dimensions at line 35. The current default size is `400x360`

🎨 **Window Color:** You can change the window's background color at line 36.

---

## Uninstallation 🗑️

If you decide to remove the clipboard manager, you can do so with the following commands:

```bash
sudo systemctl stop clipboard_monitor.service
sudo systemctl disable clipboard_monitor.service
sudo rm /etc/systemd/system/clipboard_monitor.service
sudo systemctl daemon-reload
```

To verify that the service has been successfully removed, run:

`systemctl list-units --type=service | grep clipboard_monitor
`

## Contribution 💡

Feel free to fork the project, submit issues, or contribute to the development. All ideas are welcome!


**Enjoy using your new clipboard manager! 🚀 If you run into any issues or have any feedback, don't hesitate to open a new issue on the repository**
