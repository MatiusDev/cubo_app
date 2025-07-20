#!/usr/bin/env python3
"""
Script de instalación manual para Cubo App
Para casos donde el entorno virtual no se puede crear automáticamente
"""
import os
import sys
import platform
import subprocess
from pathlib import Path

def main():
    """Función principal"""
    print("🔧 Instalación Manual de Cubo App")
    print("=" * 40)
    print()
    
    system = platform.system()
    
    if system == "Linux":
        print("🐧 Sistema Linux detectado")
        print()
        print("📋 Pasos para instalar manualmente:")
        print()
        print("1. Instalar python3-venv:")
        print("   sudo apt update")
        print("   sudo apt install python3-venv python3-pip")
        print()
        print("2. Crear entorno virtual:")
        print("   python3 -m venv venv")
        print()
        print("3. Activar entorno virtual:")
        print("   source venv/bin/activate")
        print()
        print("4. Instalar dependencias del backend:")
        print("   pip install -r backend/requirements.txt")
        print("   pip install pyinstaller requests")
        print()
        print("5. Instalar dependencias del frontend (opcional):")
        print("   cd frontend")
        print("   npm install")
        print()
        print("6. Ejecutar la aplicación:")
        print("   python run_app.py")
        print()
        
        # Preguntar si quiere ejecutar los comandos
        response = input("¿Quieres que ejecute estos comandos automáticamente? (s/n): ")
        
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            try:
                print("\n🔧 Instalando python3-venv...")
                subprocess.check_call(["sudo", "apt", "update"])
                subprocess.check_call(["sudo", "apt", "install", "-y", "python3-venv", "python3-pip"])
                
                print("🔧 Creando entorno virtual...")
                subprocess.check_call([sys.executable, "-m", "venv", "venv"])
                
                print("🔧 Activando entorno virtual...")
                venv_python = Path("venv/bin/python")
                venv_pip = Path("venv/bin/pip")
                
                print("📦 Instalando dependencias del backend...")
                subprocess.check_call([str(venv_pip), "install", "-r", "backend/requirements.txt"])
                subprocess.check_call([str(venv_pip), "install", "pyinstaller", "requests"])
                
                # Instalar dependencias del frontend si existe
                frontend_dir = Path(__file__).parent / "frontend"
                package_json = frontend_dir / "package.json"
                
                if package_json.exists():
                    print("📦 Instalando dependencias del frontend...")
                    try:
                        subprocess.check_call(["npm", "install"], cwd=frontend_dir)
                        print("✅ Dependencias del frontend instaladas")
                    except subprocess.CalledProcessError:
                        print("⚠️ Error instalando dependencias del frontend")
                        print("💡 Asegúrate de tener Node.js instalado")
                
                print("✅ Instalación completada!")
                print("\n🚀 Para ejecutar la aplicación:")
                print("   source venv/bin/activate")
                print("   python run_app.py")
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Error durante la instalación: {e}")
                print("💡 Ejecuta los comandos manualmente")
    
    elif system == "Windows":
        print("🪟 Sistema Windows detectado")
        print()
        print("📋 Pasos para instalar manualmente:")
        print()
        print("1. Crear entorno virtual:")
        print("   python -m venv venv")
        print()
        print("2. Activar entorno virtual:")
        print("   venv\\Scripts\\activate")
        print()
        print("3. Instalar dependencias del backend:")
        print("   pip install -r backend/requirements.txt")
        print("   pip install pyinstaller requests")
        print()
        print("4. Instalar dependencias del frontend (opcional):")
        print("   cd frontend")
        print("   npm install")
        print()
        print("5. Ejecutar la aplicación:")
        print("   python run_app.py")
        print()
        
        # Preguntar si quiere ejecutar los comandos
        response = input("¿Quieres que ejecute estos comandos automáticamente? (s/n): ")
        
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            try:
                print("\n🔧 Creando entorno virtual...")
                subprocess.check_call([sys.executable, "-m", "venv", "venv"])
                
                print("🔧 Activando entorno virtual...")
                venv_python = Path("venv/Scripts/python.exe")
                venv_pip = Path("venv/Scripts/pip.exe")
                
                print("📦 Instalando dependencias del backend...")
                subprocess.check_call([str(venv_pip), "install", "-r", "backend/requirements.txt"])
                subprocess.check_call([str(venv_pip), "install", "pyinstaller", "requests"])
                
                # Instalar dependencias del frontend si existe
                frontend_dir = Path(__file__).parent / "frontend"
                package_json = frontend_dir / "package.json"
                
                if package_json.exists():
                    print("📦 Instalando dependencias del frontend...")
                    try:
                        subprocess.check_call(["npm", "install"], cwd=frontend_dir)
                        print("✅ Dependencias del frontend instaladas")
                    except subprocess.CalledProcessError:
                        print("⚠️ Error instalando dependencias del frontend")
                        print("💡 Asegúrate de tener Node.js instalado")
                
                print("✅ Instalación completada!")
                print("\n🚀 Para ejecutar la aplicación:")
                print("   venv\\Scripts\\activate")
                print("   python run_app.py")
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Error durante la instalación: {e}")
                print("💡 Ejecuta los comandos manualmente")
    
    else:
        print(f"❌ Sistema operativo no soportado: {system}")
        print("💡 Solo se soportan Windows y Linux")

if __name__ == "__main__":
    main() 