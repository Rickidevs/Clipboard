import pyperclip
import time
import customtkinter as ctk
import threading
import keyboard
import sys

MAX_HISTORY = 15
WINDOW_WIDTH = 380  
WINDOW_HEIGHT = 450
BACKGROUND_COLOR = "#1F1F1F"  
BUTTON_COLOR = "#2B2B2B"     
BUTTON_HOVER = "#3A3A3A"     
ACCENT_COLOR = "#E0E0E0"      
HIGHLIGHT_COLOR = "#00ADB5"   

clipboard_history = []
history_window = None
monitor_thread_running = True

def update_clipboard_history(new_text):
    new_text = new_text.strip()
    if not new_text:
        return

    if new_text in clipboard_history:
        clipboard_history.remove(new_text)
    
    clipboard_history.insert(0, new_text)

    if len(clipboard_history) > MAX_HISTORY:
        clipboard_history.pop()

def monitor_clipboard():
    last_text = ""
    while monitor_thread_running:
        try:
            current_text = pyperclip.paste().strip()
            if current_text != last_text:
                last_text = current_text
                update_clipboard_history(current_text)
        except Exception:
            pass 
        time.sleep(0.5)

def close_window(event=None):
    global history_window
    if history_window:
        history_window.destroy()
        history_window = None

def use_clipboard_text(text):
    try:
        pyperclip.copy(text)
    finally:
        close_window()

def start_move(event):
    if history_window:
        history_window.x = event.x
        history_window.y = event.y

def do_move(event):
    if history_window:
        deltax = event.x - history_window.x
        deltay = event.y - history_window.y
        x = history_window.winfo_x() + deltax
        y = history_window.winfo_y() + deltay
        history_window.geometry(f"+{x}+{y}")

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def show_clipboard_history():
    global history_window

    if history_window is not None and history_window.winfo_exists():
        history_window.lift()
        history_window.focus_force()
        return

    history_window = ctk.CTkToplevel(root)
    history_window.title("Clipboard")
    history_window.overrideredirect(True)
    history_window.configure(fg_color=BACKGROUND_COLOR)
    history_window.attributes("-topmost", True)
    
    center_window(history_window, WINDOW_WIDTH, WINDOW_HEIGHT)

    title_bar = ctk.CTkFrame(history_window, height=40, fg_color="#181818", corner_radius=0)
    title_bar.pack(fill="x", side="top")
    
    title_bar.bind("<ButtonPress-1>", start_move)
    title_bar.bind("<B1-Motion>", do_move)

    title_label = ctk.CTkLabel(
        title_bar, 
        text="  Clipboard Manager",
        font=("Segoe UI", 13, "bold"),
        text_color="gray"
    )
    title_label.pack(side="left", padx=10)
    title_label.bind("<ButtonPress-1>", start_move)
    title_label.bind("<B1-Motion>", do_move)

    close_btn = ctk.CTkButton(
        title_bar,
        text="✕",
        width=40,
        height=40,
        fg_color="transparent",
        hover_color="#C42B1C",
        text_color="white",
        command=close_window,
        font=("Arial", 14)
    )
    close_btn.pack(side="right")


    scroll_frame = ctk.CTkScrollableFrame(
        history_window, 
        width=WINDOW_WIDTH, 
        fg_color="transparent",
        scrollbar_button_color="#333333",
        scrollbar_button_hover_color="#444444"
    )
    scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

    if not clipboard_history:
        ctk.CTkLabel(
            scroll_frame, 
            text="Pano geçmişi boş...", 
            text_color="gray",
            font=("Segoe UI", 12)
        ).pack(pady=40)
    else:
        for text in clipboard_history:
            single_line = ' '.join(text.split())
            display_text = single_line[:40] + "..." if len(single_line) > 40 else single_line

            btn = ctk.CTkButton(
                scroll_frame,
                text=display_text,
                command=lambda t=text: use_clipboard_text(t),
                fg_color=BUTTON_COLOR,
                hover_color=BUTTON_HOVER,
                text_color=ACCENT_COLOR,
                anchor="w",
                height=45,
                font=("Segoe UI", 13),
                corner_radius=6
            )
            btn.pack(fill="x", pady=3, padx=2)

    history_window.bind("<Escape>", close_window)
    history_window.focus_force()

root = ctk.CTk()
root.withdraw()

monitor_thread = threading.Thread(target=monitor_clipboard, daemon=True)
monitor_thread.start()

print("Clipboard Manager Pro Aktif.")
print("Kısayol: Ctrl + Alt + V")

try:
    keyboard.add_hotkey('ctrl + alt + v', show_clipboard_history)
except ImportError:
    print("Hata: Klavye modülü için root yetkisi gerekebilir (sudo).")

root.mainloop()
