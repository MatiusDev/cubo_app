#!/usr/bin/env python3
"""
Script completo para ejecutar Cubo App con backend y frontend Vite
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

class CuboAppFull:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
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
    
    def check_node_npm(self):
        """Verifica que Node.js y npm estén instalados"""
        try:
            subprocess.run(["node", "--version"], check=True, capture_output=True)
            subprocess.run(["npm", "--version"], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def install_frontend_dependencies(self):
        """Instala las dependencias del frontend"""
        frontend_dir = Path(__file__).parent / "frontend"
        
        if not frontend_dir.exists():
            print("❌ No se encontró el directorio frontend")
            return False
        
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print("📦 Instalando dependencias del frontend...")
            try:
                subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
                print("✅ Dependencias del frontend instaladas")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Error instalando dependencias del frontend: {e}")
                return False
        
        return True
    
    def start_backend(self):
        """Inicia el backend"""
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
            self.backend_process = subprocess.Popen([
                python_executable, str(server_script)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.is_running = True
            print("✅ Backend iniciado en http://localhost:8000")
            return True
            
        except Exception as e:
            print(f"❌ Error al ejecutar el backend: {e}")
            return False
    
    def start_frontend(self):
        """Inicia el frontend con Vite"""
        frontend_dir = Path(__file__).parent / "frontend"
        
        if not frontend_dir.exists():
            print("❌ No se encontró el directorio frontend")
            return False
        
        try:
            # Verificar dependencias
            if not self.install_frontend_dependencies():
                return False
            
            # Iniciar Vite en modo desarrollo
            print("🚀 Iniciando frontend con Vite...")
            self.frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Esperar a que Vite inicie
            time.sleep(5)
            
            if self.frontend_process.poll() is None:
                print("✅ Frontend iniciado en http://localhost:5173")
                return True
            else:
                print("❌ Error iniciando el frontend")
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando el frontend: {e}")
            return False
    
    def open_browsers(self):
        """Abre los navegadores para backend y frontend"""
        def delayed_open():
            time.sleep(8)  # Esperar a que ambos servicios inicien
            
            # Verificar si estamos en WSL2
            is_wsl2 = self.is_wsl2()
            
            if is_wsl2:
                print("💻 Detectado WSL2")
                print("🌐 Abre tu navegador en Windows y ve a:")
                print("   Frontend (Vite): http://localhost:5173")
                print("   Backend (API): http://localhost:8000")
                print()
                print("💡 Si no funciona, prueba:")
                print("   Frontend: http://127.0.0.1:5173")
                print("   Backend: http://127.0.0.1:8000")
            else:
                try:
                    webbrowser.open('http://localhost:5173')
                    print("🌐 Frontend abierto en http://localhost:5173")
                    
                    # Abrir backend en nueva pestaña
                    time.sleep(1)
                    webbrowser.open('http://localhost:8000')
                    print("🌐 Backend abierto en http://localhost:8000")
                except Exception as e:
                    print(f"⚠️ No se pudo abrir el navegador: {e}")
                    print("💡 Abre manualmente:")
                    print("   Frontend: http://localhost:5173")
                    print("   Backend: http://localhost:8000")
        
        threading.Thread(target=delayed_open, daemon=True).start()
    
    def is_wsl2(self):
        """Verifica si estamos en WSL2"""
        try:
            with open('/proc/version', 'r') as f:
                version = f.read().lower()
                return 'microsoft' in version and 'wsl' in version
        except:
            return False
    
    def signal_handler(self, signum, frame):
        """Maneja las señales de interrupción"""
        print("\n🛑 Deteniendo la aplicación...")
        self.stop()
        sys.exit(0)
    
    def stop(self):
        """Detiene la aplicación"""
        if self.backend_process and self.is_running:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend detenido")
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                print("⚠️ Backend forzado a detenerse")
            except Exception as e:
                print(f"❌ Error al detener backend: {e}")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend detenido")
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                print("⚠️ Frontend forzado a detenerse")
            except Exception as e:
                print(f"❌ Error al detener frontend: {e}")
        
        self.is_running = False
    
    def run(self):
        """Ejecuta la aplicación completa"""
        print("🚀 Iniciando Cubo App (Backend + Frontend Vite)...")
        print(f"💻 Sistema operativo: {platform.system()} {platform.release()}")
        print()
        
        # Verificar Node.js y npm
        if not self.check_node_npm():
            print("❌ Error: Node.js y npm no están instalados")
            print("💡 Instala Node.js desde https://nodejs.org")
            return
        
        # Configurar manejo de señales
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Iniciar backend
        if not self.start_backend():
            print("❌ No se pudo iniciar el backend")
            return
        
        # Iniciar frontend
        if not self.start_frontend():
            print("❌ No se pudo iniciar el frontend")
            self.stop()
            return
        
        # Abrir navegadores
        self.open_browsers()
        
        print("✅ Aplicación completa iniciada")
        print("📝 Presiona Ctrl+C para detener")
        print()
        print("🌐 URLs disponibles:")
        print("   Frontend (Vite): http://localhost:5173")
        print("   Backend (API): http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
        
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
    app = CuboAppFull()
    app.run()

if __name__ == "__main__":
    main() 