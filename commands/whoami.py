import os
import platform
import time
import psutil
import socket
from datetime import datetime
from tkinter import filedialog, Toplevel, Label
from PIL import Image, ImageTk

class UserProfile:
    def __init__(self):
        self.username = os.getlogin()  # Nombre del usuario en el sistema
        self.os_info = f"{platform.system()} {platform.release()} ({platform.architecture()[0]})"
        self.start_time = time.time()  # Guarda el tiempo en que se inició la shell
        self.profile_picture = None  # Imagen de perfil (por defecto, None)
        self.ip_address = self.get_ip_address()
        self.disk_space = self.get_disk_space()
    
    def get_uptime(self):
        """Devuelve el tiempo que la shell ha estado en uso"""
        elapsed_time = time.time() - self.start_time
        return time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    def get_ip_address(self):
        """Obtiene la dirección IP local"""
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return "No disponible"

    def get_wifi_name(self):
        """Obtiene el nombre de la red WiFi (Solo Windows)"""
        try:
            wifi_name = os.popen('netsh wlan show interfaces').read().split("SSID")[1].split(":")[1].split("\n")[0].strip()
            return wifi_name
        except:
            return "No disponible"

    def get_battery_status(self):
        """Obtiene el nivel de batería y si está cargando"""
        battery = psutil.sensors_battery()
        if battery:
            charging = "🔌 Cargando" if battery.power_plugged else "🔋 No cargando"
            return f"{battery.percent}% ({charging})"
        return "No disponible"

    def get_cpu_usage(self):
        """Obtiene el uso actual de CPU"""
        return f"{psutil.cpu_percent()}%"

    def get_ram_usage(self):
        """Obtiene el uso actual de RAM"""
        ram = psutil.virtual_memory()
        return f"{ram.used // (1024**2)} MB / {ram.total // (1024**2)} MB"

    def get_disk_space(self):
        """Obtiene el espacio en disco disponible"""
        disk = psutil.disk_usage('/')
        return f"{disk.free // (1024**3)} GB libres de {disk.total // (1024**3)} GB"

    def select_profile_picture(self):
        """Permite al usuario seleccionar una imagen como foto de perfil"""
        file_path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.profile_picture = file_path  # Guarda la ruta de la imagen
            return f"✅ Imagen de perfil seleccionada: {file_path}"
        return "❌ No se seleccionó ninguna imagen."

    def show_profile_picture(self):
        """Muestra la imagen de perfil en una ventana emergente"""
        if not self.profile_picture:
            return "❌ No hay imagen de perfil seleccionada."

        img_window = Toplevel()
        img_window.title(f"Imagen de perfil - {self.username}")

        img = Image.open(self.profile_picture)
        img = img.resize((150, 150))
        img = ImageTk.PhotoImage(img)

        img_label = Label(img_window, image=img)
        img_label.image = img
        img_label.pack()

        return "✅ Mostrando imagen de perfil."

    def get_profile_info(self):
        """Devuelve la información del usuario en un formato bonito"""
        uptime = self.get_uptime()
        wifi_name = self.get_wifi_name()
        battery_status = self.get_battery_status()
        cpu_usage = self.get_cpu_usage()
        ram_usage = self.get_ram_usage()
        
        return (
            f"👤 Usuario: {self.username}\n"
            f"💻 Sistema: {self.os_info}\n"
            f"⏳ Tiempo en sesión: {uptime}\n"
            f"🌐 IP local: {self.ip_address}\n"
            f"📶 WiFi: {wifi_name}\n"
            f"🔋 Batería: {battery_status}\n"
            f"🧠 RAM usada: {ram_usage}\n"
            f"⚙️ CPU usada: {cpu_usage}\n"
            f"💾 Espacio en disco: {self.disk_space}\n"
            f"🖼️ Imagen de perfil: {'No seleccionada' if not self.profile_picture else self.profile_picture}"
        )
