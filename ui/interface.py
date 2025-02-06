import tkinter as tk
from tkinter import scrolledtext
import subprocess
from .if_settings import change_bg_color, change_text_color, change_emoji, change_response_color
from commands.basic_commands import commands  # Diccionario de comandos internos

class RaulShell:
    def __init__(self, root):
        self.root = root
        self.root.title("RaulShell 🖥️")
        self.root.geometry("800x500")
        self.root.configure(bg="#1e1e1e")
        
        # Variables de configuración
        self.bg_color = "#1e1e1e"
        self.text_color = "#FFFFFF"    # Color para el texto general
        self.response_color = "#00FF00"  # Color predeterminado para respuestas exitosas (verde)
        self.emoji_prefix = "💻"
        
        # Historial de comandos
        self.history = []
        
        # Menú de opciones
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        
        self.settings_menu = tk.Menu(self.menu, tearoff=0)
        self.settings_menu.add_command(label="Cambiar color de fondo", command=lambda: change_bg_color(self))
        self.settings_menu.add_command(label="Cambiar color de texto", command=lambda: change_text_color(self))
        self.settings_menu.add_command(label="Cambiar emoji de prefijo", command=lambda: change_emoji(self))
        self.settings_menu.add_command(label="Cambiar color de respuesta", command=lambda: change_response_color(self))
        self.menu.add_cascade(label="Configuración", menu=self.settings_menu)
        
        # Área de salida
        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, 
                                                 bg=self.bg_color, fg=self.text_color, font=("Consolas", 12))
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        # Configurar tags para respuestas, errores y comandos
        self.output.tag_config("response", foreground=self.response_color)
        self.output.tag_config("error", foreground="red")
        self.output.tag_config("command", foreground="#FFA500")  # Naranja para los comandos ingresados
        
        # Área de entrada
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(root, textvariable=self.input_var, font=("Consolas", 12),
                                    bg="#333333", fg="#FFFFFF", insertbackground="white")
        self.input_entry.pack(fill=tk.X, padx=10, pady=5)
        self.input_entry.bind("<Return>", self.execute_command)
        
        self.print_output("🔹 Bienvenido a RaulShell v1.0 - Escribe comandos aquí 🔹")
    
    def print_output(self, text, tag=None):
        """Imprime el texto en el área de salida aplicando, si se indica, el tag para estilo."""
        self.output.insert(tk.END, text + "\n", tag)
        self.output.yview(tk.END)
    
    def execute_command(self, event=None):
        command_line = self.input_var.get().strip()
        self.input_var.set("")
        
        if command_line:
            # Agregar comando al historial
            self.history.append(command_line)
            
            # Imprime el comando ingresado (con tag "command")
            self.print_output(f"{self.emoji_prefix} > {command_line}", tag="command")
            
            # Separa el comando y sus argumentos
            parts = command_line.split()
            command = parts[0].lower()
            args = parts[1:]
            
            # Si es un comando interno, se ejecuta; de lo contrario, se envía al sistema.
            if command in commands:
                commands[command](self, *args)
            else:
                try:
                    result = subprocess.run(command_line, shell=True, capture_output=True, text=True, encoding='utf-8')
                    # Si el comando fue exitoso (código de retorno 0)
                    if result.returncode == 0:
                        output = result.stdout.strip()
                        if output:
                            self.print_output(f"✅ {output}", tag="response")
                    else:
                        output = result.stderr.strip()
                        if output:
                            self.print_output(f"❌ {output}", tag="error")
                except Exception as e:
                    self.print_output(f"❌ {str(e)}", tag="error")

def start_shell():
    import os
    os.chdir(os.path.expanduser("~"))  # Establece el directorio inicial al home del usuario
    root = tk.Tk()
    RaulShell(root)
    root.mainloop()

if __name__ == "__main__":
    start_shell()
