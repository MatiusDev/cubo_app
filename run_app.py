#!/usr/bin/env python3
"""
Script principal para ejecutar la aplicación Cubo App
Compatible con Windows y Linux
"""
import os
import sys
import platform
import subprocess
import webbrowser
import time
import signal
import threading
from pathlib import Path

class CuboApp:
    def __init__(self):
        self.process = None
        self.is_running = False
        
    def detect_os(self):
        """Detecta el sistema operativo"""
        system = platform.system().lower()
        if system == "windows":
            return "windows"
        elif system == "linux":
            return "linux"
        else:
            return "unknown"
    
    def find_executable(self):
        """Busca el ejecutable de la aplicación"""
        os_type = self.detect_os()
        current_dir = Path(__file__).parent
        
        if os_type == "windows":
            exe_name = "cubo_app.exe"
        else:
            exe_name = "cubo_app"
        
        # Buscar en diferentes ubicaciones
        possible_paths = [
            current_dir / "backend" / "dist" / exe_name,
            current_dir / "dist" / exe_name,
            current_dir / exe_name,
            current_dir / "backend" / exe_name
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
    
    def run_with_python(self):
        """Ejecuta la aplicación usando Python directamente"""
        backend_dir = Path(__file__).parent / "backend"
        server_script = backend_dir / "app" / "server.py"
        
        if not server_script.exists():
            print("❌ Error: No se encontró el script del servidor")
            return False
        
        # Buscar Python del entorno virtual
        venv_python = self.find_venv_python()
        python_executable = venv_python if venv_python else sys.executable
        
        try:
            # Cambiar al directorio del backend
            os.chdir(backend_dir)
            
            # Ejecutar el servidor
            self.process = subprocess.Popen([
                python_executable, str(server_script)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.is_running = True
            print("✅ Servidor iniciado con Python")
            return True
            
        except Exception as e:
            print(f"❌ Error al ejecutar con Python: {e}")
            return False
    
    def find_venv_python(self):
        """Busca Python del entorno virtual"""
        venv_path = Path(__file__).parent / "venv"
        
        if platform.system() == "Windows":
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            python_path = venv_path / "bin" / "python"
        
        if python_path.exists():
            return str(python_path)
        
        return None
    
    def run_executable(self):
        """Ejecuta la aplicación usando el ejecutable"""
        exe_path = self.find_executable()
        
        if not exe_path:
            print("📦 No se encontró el ejecutable compilado")
            print("💡 Esto es normal si aún no has ejecutado 'python build.py'")
            print("🔄 Intentando ejecutar con Python directamente...")
            return self.run_with_python()
        
        try:
            print(f"🚀 Ejecutando: {exe_path}")
            self.process = subprocess.Popen([str(exe_path)])
            self.is_running = True
            return True
            
        except Exception as e:
            print(f"❌ Error al ejecutar el ejecutable: {e}")
            print("🔄 Intentando ejecutar con Python...")
            return self.run_with_python()
    
    def open_browser(self):
        """Abre el navegador después de un breve delay"""
        def delayed_open():
            time.sleep(3)  # Esperar 3 segundos para que el servidor inicie
            try:
                # Verificar si estamos en WSL2 o entorno sin GUI
                if self.is_wsl2() or not self.has_display():
                    print("💻 Ejecutando en WSL2 o entorno sin GUI")
                    print("🌐 Abre manualmente en tu navegador: http://localhost:8000")
                    print("💡 Si usas WSL2, puedes acceder desde Windows en: http://localhost:8000")
                else:
                    webbrowser.open('http://localhost:8000')
                    print("🌐 Navegador abierto en http://localhost:8000")
            except Exception as e:
                print(f"⚠️ No se pudo abrir el navegador automáticamente: {e}")
                print("💡 Abre manualmente: http://localhost:8000")
        
        threading.Thread(target=delayed_open, daemon=True).start()
    
    def is_wsl2(self):
        """Verifica si estamos en WSL2"""
        try:
            with open('/proc/version', 'r') as f:
                version = f.read().lower()
                return 'microsoft' in version and 'wsl' in version
        except:
            return False
    
    def has_display(self):
        """Verifica si hay una pantalla disponible"""
        return 'DISPLAY' in os.environ or 'WAYLAND_DISPLAY' in os.environ
    
    def signal_handler(self, signum, frame):
        """Maneja las señales de interrupción"""
        print("\n🛑 Deteniendo la aplicación...")
        self.stop()
        sys.exit(0)
    
    def stop(self):
        """Detiene la aplicación"""
        if self.process and self.is_running:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                print("✅ Aplicación detenida")
            except subprocess.TimeoutExpired:
                self.process.kill()
                print("⚠️ Aplicación forzada a detenerse")
            except Exception as e:
                print(f"❌ Error al detener: {e}")
        
        self.is_running = False
    
    def run(self):
        """Ejecuta la aplicación principal"""
        print("🚀 Iniciando Cubo App...")
        print(f"💻 Sistema operativo: {platform.system()} {platform.release()}")
        
        # Verificar si hay un frontend de Vite
        frontend_dir = Path(__file__).parent / "frontend"
        package_json = frontend_dir / "package.json"
        
        if package_json.exists():
            try:
                import json
                with open(package_json, 'r') as f:
                    package_data = json.load(f)
                
                # Verificar si tiene scripts de Vite
                if 'scripts' in package_data and 'dev' in package_data['scripts']:
                    print("🎨 Frontend de Vite detectado")
                    print("🔄 Usando modo completo (Backend + Frontend Vite)")
                    print()
                    
                    # Importar y ejecutar el script completo
                    from run_app_full import CuboAppFull
                    app_full = CuboAppFull()
                    app_full.run()
                    return
            except Exception as e:
                print(f"⚠️ Error detectando frontend: {e}")
        
        # Configurar manejo de señales
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Intentar ejecutar el ejecutable primero
        if not self.run_executable():
            print("❌ No se pudo iniciar la aplicación")
            return
        
        # Abrir navegador
        self.open_browser()
        
        print("✅ Aplicación iniciada correctamente")
        print("📝 Presiona Ctrl+C para detener")
        print()
        print("💡 Para crear un ejecutable independiente:")
        print("   python build.py")
        print("   Luego podrás ejecutar: ./backend/dist/cubo_app")
        
        try:
            # Mantener la aplicación corriendo
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Interrupción detectada")
        finally:
            self.stop()

def main():
    """Función principal"""
    app = CuboApp()
    app.run()

if __name__ == "__main__":
    main() 