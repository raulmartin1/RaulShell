import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

def open_advanced_config_panel(shell):
    panel = tk.Toplevel(shell.root)
    panel.title("Configuración Avanzada")
    panel.geometry("500x450")
    
    # --- Sección de Alias de Comandos ---
    alias_frame = tk.LabelFrame(panel, text="Alias de Comandos", padx=10, pady=10)
    alias_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Label(alias_frame, text="Comando:").grid(row=0, column=0, sticky="w")
    tk.Label(alias_frame, text="Alias:").grid(row=0, column=1, sticky="w")
    
    alias_entry_command = tk.Entry(alias_frame)
    alias_entry_command.grid(row=1, column=0, padx=5, pady=5)
    alias_entry_alias = tk.Entry(alias_frame)
    alias_entry_alias.grid(row=1, column=1, padx=5, pady=5)
    
    def save_alias():
        cmd = alias_entry_command.get().strip()
        alias = alias_entry_alias.get().strip()
        if cmd and alias:
            if not hasattr(shell, "aliases"):
                shell.aliases = {}
            shell.aliases[alias] = cmd
            shell.print_output(f"Alias guardado: {alias} => {cmd}")
            alias_entry_command.delete(0, tk.END)
            alias_entry_alias.delete(0, tk.END)
    
    tk.Button(alias_frame, text="Guardar Alias", command=save_alias).grid(row=2, column=0, columnspan=2, pady=5)
    
    # --- Sección de Estilo de Fuente ---
    font_frame = tk.LabelFrame(panel, text="Estilo de Fuente", padx=10, pady=10)
    font_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Label(font_frame, text="Familia de Fuente:").grid(row=0, column=0, sticky="w")
    available_fonts = list(tkFont.families())
    available_fonts.sort()
    font_family_var = tk.StringVar(value=getattr(shell, "font_family", "Consolas"))
    font_family_combo = ttk.Combobox(font_frame, textvariable=font_family_var, values=available_fonts, state="readonly")
    font_family_combo.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(font_frame, text="Tamaño de Fuente:").grid(row=1, column=0, sticky="w")
    font_size_var = tk.IntVar(value=getattr(shell, "font_size", 12))
    font_size_spinbox = tk.Spinbox(font_frame, from_=8, to=40, textvariable=font_size_var)
    font_size_spinbox.grid(row=1, column=1, padx=5, pady=5)
    
    def apply_font_change():
        new_family = font_family_var.get()
        new_size = font_size_var.get()
        new_font = (new_family, new_size)
        shell.font_family = new_family
        shell.font_size = new_size
        shell.output.configure(font=new_font)
        shell.input_entry.configure(font=new_font)
        shell.print_output(f"Estilo de fuente cambiado a {new_family} {new_size}")
    
    tk.Button(font_frame, text="Aplicar Fuente", command=apply_font_change).grid(row=2, column=0, columnspan=2, pady=5)
    
    # --- Sección de Tamaño de la Ventana ---
    window_frame = tk.LabelFrame(panel, text="Tamaño de la Ventana", padx=10, pady=10)
    window_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Label(window_frame, text="Ancho:").grid(row=0, column=0, sticky="w")
    width_var = tk.IntVar(value=shell.root.winfo_width())
    tk.Entry(window_frame, textvariable=width_var).grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(window_frame, text="Alto:").grid(row=1, column=0, sticky="w")
    height_var = tk.IntVar(value=shell.root.winfo_height())
    tk.Entry(window_frame, textvariable=height_var).grid(row=1, column=1, padx=5, pady=5)
    
    def apply_window_size():
        new_width = width_var.get()
        new_height = height_var.get()
        shell.root.geometry(f"{new_width}x{new_height}")
        shell.print_output(f"Tamaño de ventana actualizado a {new_width}x{new_height}.")
    
    tk.Button(window_frame, text="Aplicar Tamaño", command=apply_window_size).grid(row=2, column=0, columnspan=2, pady=5)
    
    # --- Sección para Activar/Desactivar Módulos ---
    modules_frame = tk.LabelFrame(panel, text="Módulos", padx=10, pady=10)
    modules_frame.pack(fill="x", padx=10, pady=5)
    
    autocomp_var = tk.BooleanVar(value=getattr(shell, "autocompletion_enabled", True))
    tk.Checkbutton(modules_frame, text="Activar Autocompletado", variable=autocomp_var).pack(anchor="w")
    
    def apply_modules():
        shell.autocompletion_enabled = autocomp_var.get()
        estado = "activado" if autocomp_var.get() else "desactivado"
        shell.print_output(f"Autocompletado {estado}.")
    
    tk.Button(modules_frame, text="Aplicar Módulos", command=apply_modules).pack(pady=5)
    
    tk.Button(panel, text="Cerrar", command=panel.destroy).pack(pady=10)
