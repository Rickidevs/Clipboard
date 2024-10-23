import pyperclip
import time
import customtkinter as ctk
import threading
import keyboard

clipboard_history = []

def update_clipboard_history(new_text):
    new_text = new_text.strip()

    if new_text in clipboard_history or new_text == "":
        return

    clipboard_history.insert(0, new_text)

    if len(clipboard_history) > 10:
        clipboard_history.pop()

def monitor_clipboard():
    last_text = ""
    while True:
        current_text = pyperclip.paste().strip()
        
        if current_text != last_text:
            last_text = current_text
            update_clipboard_history(current_text)

        time.sleep(0.5)

def show_clipboard_history():
    global history_window
    history_window = ctk.CTkToplevel(root)
    history_window.title("Clipboard History")
    history_window.geometry("400x450")
    history_window.configure(fg_color="#424242")

    for widget in history_window.winfo_children():
        widget.destroy()

    if not clipboard_history:
        print("could not find clipboard history")
        return

    for text in clipboard_history:
        single_line_text = ' '.join(text.split())
        short_text = single_line_text if len(single_line_text) <= 40 else single_line_text[:40] + '...'

        button = ctk.CTkButton(
            history_window,
            text=short_text,
            command=lambda t=text: use_clipboard_text(t, history_window),
            fg_color="#4D4D4D",
            border_color="white",
            border_width=1,
            hover_color="#494949",
            anchor='w'
        )
        
        button.pack(fill='x', padx=10, pady=(5, 0))
def use_clipboard_text(text, window):
    pyperclip.copy(text)
    window.destroy()

root = ctk.CTk()
root.withdraw() 
root.resizable(True, True)

monitor_clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
monitor_clipboard_thread.start()

keyboard.add_hotkey('ctrl + alt + v', show_clipboard_history)

root.mainloop()
