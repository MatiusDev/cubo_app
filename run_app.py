#!/usr/bin/env python3
"""
Script unificado para ejecutar Cubo App
Controlado por config.env
"""
import os
import sys
import platform
import subprocess
import webbrowser
import time
import signal
import threading
import requests
from pathlib import Path

# Importar configuración
from config import config

class CuboAppUnified:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.is_running = False
        
    def detect_wsl(self):
        """Detecta si estamos en WSL"""
        if not config.wsl_detection:
            return False
            
        try:
            with open('/proc/version', 'r') as f:
                version = f.read().lower()
                return 'microsoft' in version and 'wsl' in version
        except:
            return False
    
    def get_windows_ip(self):
        """Obtiene la IP de Windows desde WSL"""
        try:
            result = subprocess.run(['cat', '/etc/resolv.conf'], 
                                  capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if line.startswith('nameserver'):
                    return line.split()[1]
        except:
            pass
        return 'localhost'
    
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
            subprocess.run(["node", "--version"], check=True, capture_output=True, timeout=10)
            subprocess.run(["npm", "--version"], check=True, capture_output=True, timeout=10)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def install_frontend_dependencies(self):
        """Instala las dependencias del frontend"""
        frontend_dir = Path(__file__).parent / "frontend"
        
        if not frontend_dir.exists():
            config.log("Directorio frontend no encontrado")
            return False
        
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print("📦 Instalando dependencias del frontend...")
            try:
                subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, timeout=300)
                print("✅ Dependencias del frontend instaladas")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Error instalando dependencias del frontend: {e}")
                return False
            except subprocess.TimeoutExpired:
                print("❌ Timeout instalando dependencias del frontend")
                return False
        
        return True
    
    def start_backend(self):
        """Inicia el backend"""
        if not config.is_backend_mode():
            config.log("Modo backend no habilitado")
            return True
        
        backend_dir = Path(__file__).parent / "backend"
        server_script = backend_dir / "app" / "server.py"
        
        if not server_script.exists():
            print("❌ Error: No se encontró el script del servidor")
            print(f"💡 Buscando en: {server_script}")
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
            print(f"✅ Backend iniciado en {config.get_backend_url()}")
            return True
            
        except Exception as e:
            print(f"❌ Error al ejecutar el backend: {e}")
            return False
    
    def wait_for_backend(self, timeout=30):
        """Espera a que el backend esté listo"""
        if not config.is_backend_mode():
            return True
            
        print("⏳ Esperando a que el backend esté listo...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(config.get_backend_url(), timeout=5)
                if response.status_code == 200:
                    print("✅ Backend listo")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(1)
        
        print("❌ Timeout esperando al backend")
        return False
    
    def start_frontend(self):
        """Inicia el frontend"""
        if not config.is_frontend_mode():
            config.log("Modo frontend no habilitado")
            return True
        
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
                print(f"✅ Frontend iniciado en {config.get_frontend_url()}")
                self.is_running = True  # <-- Asegura que el bucle principal siga activo
                return True
            else:
                stdout, stderr = self.frontend_process.communicate()
                print("❌ Error iniciando el frontend")
                if stderr:
                    print(f"Error: {stderr.decode()}")
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando el frontend: {e}")
            return False
    
    def wait_for_frontend(self, timeout=30):
        """Espera a que el frontend esté listo"""
        if not config.is_frontend_mode():
            return True
            
        print("⏳ Esperando a que el frontend esté listo...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(config.get_frontend_url(), timeout=5)
                if response.status_code == 200:
                    print("✅ Frontend listo")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(1)
        
        print("❌ Timeout esperando al frontend")
        return False
    
    def open_browsers(self):
        """Abre los navegadores según la configuración"""
        if not config.auto_open_browser:
            config.log("Auto-open browser deshabilitado")
            return
            
        def delayed_open():
            # Esperar a que los servicios estén listos
            backend_ready = self.wait_for_backend()
            frontend_ready = self.wait_for_frontend()
            
            if not backend_ready and config.is_backend_mode():
                print("⚠️ Backend no está listo")
            
            if not frontend_ready and config.is_frontend_mode():
                print("⚠️ Frontend no está listo")
            
            # Verificar si estamos en WSL2
            is_wsl2 = self.detect_wsl()
            
            if is_wsl2:
                print("💻 Detectado WSL2")
                print("🌐 Abre tu navegador en Windows y ve a:")
                if config.is_backend_mode():
                    print(f"   Backend: {config.get_backend_url()}")
                if config.is_frontend_mode():
                    print(f"   Frontend: {config.get_frontend_url()}")
            else:
                try:
                    if config.is_frontend_mode():
                        webbrowser.open(config.get_frontend_url())
                        print(f"🌐 Frontend abierto en {config.get_frontend_url()}")
                    
                    if config.is_backend_mode():
                        time.sleep(1)
                        webbrowser.open(config.get_backend_url())
                        print(f"🌐 Backend abierto en {config.get_backend_url()}")
                except Exception as e:
                    print(f"⚠️ No se pudo abrir el navegador: {e}")
                    print("💡 Abre manualmente:")
                    if config.is_backend_mode():
                        print(f"   Backend: {config.get_backend_url()}")
                    if config.is_frontend_mode():
                        print(f"   Frontend: {config.get_frontend_url()}")
        
        threading.Thread(target=delayed_open, daemon=True).start()
    
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
        """Ejecuta la aplicación según la configuración"""
        print("🚀 Iniciando Cubo App (Unificado)...")
        print(f"💻 Sistema operativo: {platform.system()} {platform.release()}")
        
        # Mostrar configuración
        config.print_config()
        
        # Verificar Node.js si se necesita frontend
        if config.is_frontend_mode():
            if not self.check_node_npm():
                print("❌ Error: Node.js y npm no están instalados")
                print("💡 Instala Node.js desde https://nodejs.org")
                return
        
        # Configurar manejo de señales
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Iniciar componentes según configuración
        if config.is_backend_mode():
            if not self.start_backend():
                print("❌ No se pudo iniciar el backend")
                return
        
        if config.is_frontend_mode():
            if not self.start_frontend():
                print("❌ No se pudo iniciar el frontend")
                if config.is_backend_mode():
                    self.stop()
                return
        
        # Abrir navegadores
        self.open_browsers()
        
        print("✅ Aplicación iniciada correctamente")
        print("📝 Presiona Ctrl+C para detener")
        print()
        
        # Mostrar URLs disponibles
        print("🌐 URLs disponibles:")
        if config.is_backend_mode():
            print(f"   Backend: {config.get_backend_url()}")
            print(f"   API Docs: {config.get_backend_url()}/docs")
        if config.is_frontend_mode():
            print(f"   Frontend: {config.get_frontend_url()}")
        
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
    app = CuboAppUnified()
    app.run()

if __name__ == "__main__":
    main() 