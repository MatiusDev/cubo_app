#!/usr/bin/env python3
"""
Script para construir el ejecutable de Cubo App
Compatible con Windows y Linux
"""
import os
import sys
import platform
import subprocess
from pathlib import Path

def install_dependencies():
    """Instala las dependencias necesarias"""
    print("📦 Instalando dependencias...")
    
    # Buscar Python del entorno virtual
    venv_path = Path(__file__).parent / "venv"
    
    if platform.system() == "Windows":
        pip_executable = venv_path / "Scripts" / "pip.exe"
    else:
        pip_executable = venv_path / "bin" / "pip"
    
    if not pip_executable.exists():
        print("❌ No se encontró el entorno virtual")
        print("💡 Ejecuta primero: python install.py")
        return False
    
    # Instalar dependencias del backend
    backend_dir = Path(__file__).parent / "backend"
    requirements_file = backend_dir / "requirements.txt"
    
    if requirements_file.exists():
        try:
            subprocess.check_call([
                str(pip_executable), "install", "-r", str(requirements_file)
            ])
            print("✅ Dependencias del backend instaladas")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando dependencias del backend: {e}")
            return False
    
    # Instalar PyInstaller
    try:
        subprocess.check_call([
            str(pip_executable), "install", "pyinstaller"
        ])
        print("✅ PyInstaller instalado")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando PyInstaller: {e}")
        return False
    
    return True

def build_executable():
    """Construye el ejecutable"""
    print("🔨 Construyendo ejecutable...")
    
    # Ejecutar el script de construcción del backend
    build_script = Path(__file__).parent / "backend" / "build_exe.py"
    
    if build_script.exists():
        try:
            subprocess.check_call([sys.executable, str(build_script)])
            print("✅ Ejecutable construido exitosamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error construyendo ejecutable: {e}")
            return False
    else:
        print("❌ No se encontró el script de construcción")
        return False

def create_launcher():
    """Crea un launcher simple"""
    print("🎯 Creando launcher...")
    
    # Crear un launcher simple que ejecute run_app.py
    launcher_content = '''#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

# Ejecutar el script principal
script_path = Path(__file__).parent / "run_app.py"
subprocess.run([sys.executable, str(script_path)])
'''
    
    launcher_path = Path(__file__).parent / "launcher.py"
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    # Hacer ejecutable en Linux
    if platform.system() != "Windows":
        os.chmod(launcher_path, 0o755)
    
    print("✅ Launcher creado")

def main():
    """Función principal"""
    print("🚀 Iniciando construcción de Cubo App...")
    print(f"💻 Sistema operativo: {platform.system()} {platform.release()}")
    print()
    
    # Instalar dependencias
    if not install_dependencies():
        print("❌ Error instalando dependencias")
        sys.exit(1)
    
    # Construir ejecutable
    if not build_executable():
        print("❌ Error construyendo ejecutable")
        sys.exit(1)
    
    # Crear launcher
    create_launcher()
    
    print()
    print("🎉 ¡Construcción completada!")
    print()
    print("📁 Archivos generados:")
    print("   - backend/dist/cubo_app (Linux) o cubo_app.exe (Windows)")
    print("   - run_app.py (script principal)")
    print("   - run_app.bat (Windows)")
    print("   - run_app.sh (Linux)")
    print("   - launcher.py (launcher simple)")
    print()
    print("🚀 Para ejecutar la aplicación:")
    if platform.system() == "Windows":
        print("   - Doble clic en run_app.bat")
        print("   - O ejecuta: python run_app.py")
    else:
        print("   - Ejecuta: ./run_app.sh")
        print("   - O ejecuta: python3 run_app.py")

if __name__ == "__main__":
    main() 