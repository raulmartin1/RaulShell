import tkinter as tk
from tkinter import colorchooser, ttk

def change_bg_color(shell):
    color = colorchooser.askcolor()[1]
    if color:
        shell.bg_color = color
        shell.output.configure(bg=shell.bg_color)
        shell.root.configure(bg=shell.bg_color)

def change_text_color(shell):
    color = colorchooser.askcolor()[1]
    if color:
        shell.text_color = color
        shell.output.configure(fg=shell.text_color)

def change_emoji(shell):
    emoji_window = tk.Toplevel(shell.root)
    emoji_window.title("Seleccionar Emoji")
    emoji_window.geometry("300x150")
    
    emojis = ["💻", "🚀", "🔥", "🛠️", "🔫", "😎", "⚡", "👨‍💻"]
    selected_emoji = tk.StringVar(value=shell.emoji_prefix)
    
    tk.Label(emoji_window, text="Selecciona un emoji:").pack(pady=5)
    emoji_dropdown = ttk.Combobox(emoji_window, values=emojis, textvariable=selected_emoji, state="readonly")
    emoji_dropdown.pack(pady=5)
    
    def set_emoji():
        shell.emoji_prefix = selected_emoji.get()
        emoji_window.destroy()
    
    tk.Button(emoji_window, text="Aceptar", command=set_emoji).pack(pady=10)
