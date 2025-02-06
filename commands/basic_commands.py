import os
import tkinter as tk
import datetime

def clear_command(shell, *args):
    """Limpia la pantalla de salida."""
    shell.output.delete("1.0", tk.END)
    shell.print_output("✅ Pantalla limpia.")

def help_command(shell, *args):
    """Muestra los comandos disponibles."""
    help_text = (
        "Comandos disponibles:\n"
        "  clear    - Limpia la pantalla.\n"
        "  help     - Muestra este mensaje de ayuda.\n"
        "  version  - Muestra la versión de RaulShell.\n"
        "  cd       - Cambia el directorio actual. Uso: cd <ruta>\n"
        "  ls       - Lista archivos y carpetas del directorio actual.\n"
        "  echo     - Imprime un mensaje. Uso: echo <mensaje>\n"
        "  date     - Muestra la fecha y hora actual.\n"
        "  history  - Muestra el historial de comandos.\n"
        "  (Si el comando no es interno, se ejecuta en el sistema.)"
    )
    shell.print_output(help_text)

def version_command(shell, *args):
    """Muestra la versión de la shell."""
    shell.print_output("RaulShell v1.0")

def cd_command(shell, *args):
    """Cambia el directorio actual. Uso: cd <ruta>"""
    if not args:
        shell.print_output("Uso: cd <ruta>")
    else:
        try:
            os.chdir(args[0])
            shell.print_output(f"✅ Directorio cambiado a: {os.getcwd()}")
        except Exception as e:
            shell.print_output(f"❌ Error: {str(e)}")

def ls_command(shell, *args):
    """Lista los archivos y carpetas del directorio actual."""
    try:
        files = os.listdir(os.getcwd())
        if files:
            shell.print_output("\n".join(files))
        else:
            shell.print_output("Directorio vacío.")
    except Exception as e:
        shell.print_output(f"❌ Error: {str(e)}")

def echo_command(shell, *args):
    """Imprime un mensaje. Uso: echo <mensaje>"""
    shell.print_output(" ".join(args))

def date_command(shell, *args):
    """Muestra la fecha y hora actual."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    shell.print_output(now)

def history_command(shell, *args):
    """Muestra el historial de comandos."""
    if shell.history:
        shell.print_output("Historial de comandos:")
        for idx, cmd in enumerate(shell.history, 1):
            shell.print_output(f"{idx}. {cmd}")
    else:
        shell.print_output("Historial vacío.")

# Diccionario que asocia nombres de comandos con sus funciones.
commands = {
    "clear": clear_command,
    "help": help_command,
    "version": version_command,
    "cd": cd_command,
    "ls": ls_command,
    "echo": echo_command,
    "date": date_command,
    "history": history_command,
}
