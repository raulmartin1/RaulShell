import socket
import speedtest
import platform
import subprocess
import requests
import re

def checknet_command(shell, *args):
    """Verifica si hay conexión a Internet."""
    try:
        requests.get("https://www.google.com", timeout=5)
        shell.print_output("✅ Conexión a Internet: ACTIVA")
    except requests.ConnectionError:
        shell.print_output("❌ No hay conexión a Internet.")

def format_network_output(output):
    """Formatea la salida de ipconfig para que sea más legible."""
    lines = output.split("\n")
    formatted_output = []

    for line in lines:
        clean_line = re.sub(r'\s+', ' ', line).strip()
        clean_line = clean_line.replace(":", " ➜")  # Agrega un separador visual
        if clean_line:
            formatted_output.append(f"   {clean_line}")  # Indentación para mejor visibilidad

    return "\n".join(formatted_output)

def netinfo_command(shell, *args):
    """Muestra información sobre la red con formato limpio."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        shell.print_output("═══════════════════════════════════")
        shell.print_output(" 🌐 INFORMACIÓN DE RED")
        shell.print_output("═══════════════════════════════════")
        shell.print_output(f" 🔹 Nombre del equipo  : {hostname}")
        shell.print_output(f" 📡 Dirección IP Local : {local_ip}")

        if platform.system() == "Windows":
            result = subprocess.run(["ipconfig"], capture_output=True, text=True)
            formatted_output = format_network_output(result.stdout)
            shell.print_output("\n📡 ADAPTADORES DE RED:")
            shell.print_output("───────────────────────────────────")
            shell.print_output(formatted_output)
        else:
            result = subprocess.run(["ifconfig"], capture_output=True, text=True)
            shell.print_output("\n📡 INFORMACIÓN DE RED:")
            shell.print_output("───────────────────────────────────")
            shell.print_output(result.stdout)

    except Exception as e:
        shell.print_output(f"❌ Error al obtener información de la red: {str(e)}")

def speedtest_command(shell, *args):
    """Realiza una prueba de velocidad de Internet."""
    shell.print_output("📶 Ejecutando SpeedTest...")

    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        download_speed = st.download() / 1_000_000  # Convertir a Mbps
        upload_speed = st.upload() / 1_000_000  # Convertir a Mbps
        ping = st.results.ping

        shell.print_output("\n═══════════════════════════════════")
        shell.print_output(" 📊 RESULTADOS DEL SPEEDTEST")
        shell.print_output("═══════════════════════════════════")
        shell.print_output(f" 📥 Descarga : {download_speed:.2f} Mbps")
        shell.print_output(f" 📤 Subida   : {upload_speed:.2f} Mbps")
        shell.print_output(f" 📡 Latencia : {ping} ms")

    except Exception as e:
        shell.print_output(f"❌ Error en SpeedTest: {str(e)}")

# Diccionario de comandos de red
network_commands = {
    "checknet": checknet_command,   # Verificar conexión a Internet
    "netinfo": netinfo_command,     # Mostrar información de red
    "speedtest": speedtest_command  # Test de velocidad
}
