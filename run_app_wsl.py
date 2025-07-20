#!/usr/bin/env python3
"""
Script específico para ejecutar Cubo App en WSL2
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

class CuboAppWSL:
    def __init__(self):
        self.process = None
        self.is_running = False
        
    def detect_wsl(self):
        """Detecta si estamos en WSL"""
        try:
            with open('/proc/version', 'r') as f:
                version = f.read().lower()
                return 'microsoft' in version and 'wsl' in version
        except:
            return False
    
    def get_windows_ip(self):
        """Obtiene la IP de Windows desde WSL"""
        try:
            # Obtener la IP del host Windows
            result = subprocess.run(['cat', '/etc/resolv.conf'], 
                                  capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if line.startswith('nameserver'):
                    return line.split()[1]
        except:
            pass
        return 'localhost'
    
    def run_with_python(self):
        """Ejecuta la aplicación usando Python"""
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
    
    def open_browser_wsl(self):
        """Abre el navegador específicamente para WSL2"""
        def delayed_open():
            time.sleep(3)  # Esperar 3 segundos para que el servidor inicie
            
            if self.detect_wsl():
                windows_ip = self.get_windows_ip()
                print("💻 Detectado WSL2")
                print(f"🌐 Abre tu navegador en Windows y ve a:")
                print(f"   http://localhost:8000")
                print(f"   o http://{windows_ip}:8000")
                print()
                print("💡 Si no funciona, prueba:")
                print("   1. http://localhost:8000")
                print("   2. http://127.0.0.1:8000")
                print("   3. http://{windows_ip}:8000")
            else:
                try:
                    webbrowser.open('http://localhost:8000')
                    print("🌐 Navegador abierto en http://localhost:8000")
                except Exception as e:
                    print(f"⚠️ No se pudo abrir el navegador: {e}")
                    print("💡 Abre manualmente: http://localhost:8000")
        
        threading.Thread(target=delayed_open, daemon=True).start()
    
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
        print("🚀 Iniciando Cubo App en WSL2...")
        print(f"💻 Sistema operativo: {platform.system()} {platform.release()}")
        
        if self.detect_wsl():
            print("✅ WSL2 detectado")
        else:
            print("⚠️ No se detectó WSL2, pero continuando...")
        
        print()
        
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
        
        # Ejecutar con Python
        if not self.run_with_python():
            print("❌ No se pudo iniciar la aplicación")
            return
        
        # Abrir navegador
        self.open_browser_wsl()
        
        print("✅ Aplicación iniciada correctamente")
        print("📝 Presiona Ctrl+C para detener")
        print()
        print("💡 Para crear un ejecutable independiente:")
        print("   python build.py")
        
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
    app = CuboAppWSL()
    app.run()

if __name__ == "__main__":
    main() 