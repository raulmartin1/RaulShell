import platform
import subprocess
import psutil
import time
from datetime import timedelta

def get_processor_info():
    """Obtiene información del procesador."""
    cpu_name = platform.processor()
    physical_cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)
    return f"⚙️ Procesador:\n   - Modelo: {cpu_name}\n   - Núcleos: {physical_cores} físicos / {logical_cores} hilos"

def get_gpu_info():
    """Obtiene información de la tarjeta gráfica en Windows usando WMIC."""
    try:
        output = subprocess.check_output("wmic path win32_videocontroller get name", shell=True)
        lines = output.decode().strip().split("\n")
        gpu_names = [line.strip() for line in lines[1:] if line.strip()]
        if gpu_names:
            return "\n".join([f"🎮 Tarjeta Gráfica:\n   - Modelo: {gpu}" for gpu in gpu_names])
        return "🎮 Tarjeta Gráfica: No detectada"
    except Exception as e:
        return f"❌ Error al obtener la GPU: {str(e)}"

def get_memory_info():
    """Obtiene información de la memoria RAM."""
    ram = psutil.virtual_memory()
    total_ram = ram.total // (1024**3)
    available_ram = ram.available // (1024**3)
    return f"💾 Memoria RAM:\n   - Total: {total_ram} GB\n   - Disponible: {available_ram} GB"

def get_system_info():
    """Obtiene información del sistema operativo."""
    os_name = platform.system()
    os_version = platform.version()
    os_arch = platform.architecture()[0]
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_str = str(timedelta(seconds=int(uptime_seconds)))
    return f"🖥️ Sistema Operativo:\n   - Nombre: {os_name} ({os_arch})\n   - Versión: {os_version}\n   - Tiempo de actividad: {uptime_str}"

def sysinfo_command(shell, *args):
    """Comando sysinfo para mostrar información del sistema."""
    sysinfo = "\n".join([
        get_processor_info(),
        get_gpu_info(),
        get_memory_info(),
        get_system_info()
    ])
    shell.print_output(sysinfo)

