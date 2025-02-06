import tkinter as tk

def clear_command(shell, *args):
    """Limpia la pantalla de salida."""
    shell.output.delete("1.0", tk.END)
    shell.print_output("✅ Pantalla limpia.")

def help_command(shell, *args):
    """Muestra los comandos disponibles."""
    help_text = (
        "Comandos disponibles:\n"
        "  clear   - Limpia la pantalla.\n"
        "  help    - Muestra este mensaje de ayuda.\n"
        "  version - Muestra la versión de RaulShell.\n"
        "  (Si el comando no es interno, se ejecuta en el sistema.)"
    )
    shell.print_output(help_text)

def version_command(shell, *args):
    """Muestra la versión de la shell."""
    shell.print_output("RaulShell v1.0")

# Diccionario que relaciona nombres de comandos con sus funciones.
commands = {
    "clear": clear_command,
    "help": help_command,
    "version": version_command,
}
