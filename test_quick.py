#!/usr/bin/env python3
"""
Prueba rápida de la aplicación Cubo App
"""
import requests
import time
import subprocess
import sys
import threading
from pathlib import Path

def test_server():
    """Prueba el servidor"""
    print("🧪 Probando servidor...")
    
    # Buscar Python del entorno virtual
    venv_path = Path(__file__).parent / "venv"
    if platform.system() == "Windows":
        python_executable = venv_path / "Scripts" / "python.exe"
    else:
        python_executable = venv_path / "bin" / "python"
    
    if not python_executable.exists():
        print("❌ No se encontró el entorno virtual")
        print("💡 Ejecuta: python install.py")
        return False
    
    # Iniciar servidor
    backend_dir = Path(__file__).parent / "backend"
    server_script = backend_dir / "app" / "server.py"
    
    try:
        # Cambiar al directorio del backend
        import os
        os.chdir(backend_dir)
        
        # Iniciar servidor en segundo plano
        process = subprocess.Popen([
            str(python_executable), str(server_script)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar a que inicie
        time.sleep(5)
        
        # Probar endpoints
        try:
            response = requests.get("http://localhost:8000/", timeout=10)
            if response.status_code == 200:
                print("✅ Servidor responde correctamente")
                
                response = requests.get("http://localhost:8000/items", timeout=10)
                if response.status_code == 200:
                    print("✅ API funciona correctamente")
                    print("🎉 ¡Aplicación funcionando perfectamente!")
                    return True
                else:
                    print("❌ Error en endpoint /items")
                    return False
            else:
                print("❌ Error en endpoint /")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error conectando al servidor: {e}")
            return False
            
        finally:
            # Detener servidor
            process.terminate()
            process.wait()
    
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Prueba Rápida de Cubo App")
    print("=" * 30)
    print()
    
    if test_server():
        print()
        print("✅ ¡Todo funciona correctamente!")
        print("🚀 Puedes ejecutar la aplicación con:")
        print("   python run_app.py")
        print("   o ./run_app.sh")
    else:
        print()
        print("❌ Algunos problemas detectados")
        print("💡 Revisa la instalación con: python install.py")

if __name__ == "__main__":
    import platform
    main() 