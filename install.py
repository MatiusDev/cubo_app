#!/usr/bin/env python3
"""
Script de instalación rápida para Cubo App
"""
import os
import sys
import platform
import subprocess
from pathlib import Path

def check_python():
    """Verifica que Python esté instalado"""
    print("🐍 Verificando Python...")
    
    try:
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print(f"❌ Python {version.major}.{version.minor} no es compatible")
            print("💡 Se requiere Python 3.8 o superior")
            return False
        
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando Python: {e}")
        return False

def check_node_npm():
    """Verifica que Node.js y npm estén instalados"""
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_dependencies():
    """Instala las dependencias"""
    print("📦 Instalando dependencias...")
    
    backend_dir = Path(__file__).parent / "backend"
    requirements_file = backend_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ No se encontró requirements.txt")
        return False
    
    # Crear entorno virtual
    venv_path = Path(__file__).parent / "venv"
    
    if not venv_path.exists():
        print("🔧 Creando entorno virtual...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "venv", str(venv_path)
            ])
            print("✅ Entorno virtual creado")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creando entorno virtual: {e}")
            print("💡 Instala python3-venv: sudo apt install python3-venv")
            return False
    
    # Determinar el ejecutable de pip del entorno virtual
    if platform.system() == "Windows":
        pip_executable = venv_path / "Scripts" / "pip.exe"
        python_executable = venv_path / "Scripts" / "python.exe"
    else:
        pip_executable = venv_path / "bin" / "pip"
        python_executable = venv_path / "bin" / "python"
    
    try:
        # Instalar dependencias en el entorno virtual
        subprocess.check_call([
            str(pip_executable), "install", "-r", str(requirements_file)
        ])
        print("✅ Dependencias del backend instaladas")
        
        # Instalar PyInstaller
        subprocess.check_call([
            str(pip_executable), "install", "pyinstaller"
        ])
        print("✅ PyInstaller instalado")
        
        # Instalar requests para pruebas
        subprocess.check_call([
            str(pip_executable), "install", "requests"
        ])
        print("✅ Requests instalado")
        
        # Instalar dependencias del frontend (si existe)
        frontend_dir = Path(__file__).parent / "frontend"
        package_json = frontend_dir / "package.json"
        
        if package_json.exists():
            print("🎨 Frontend detectado, verificando Node.js...")
            
            if not check_node_npm():
                print("❌ Node.js y npm no están instalados")
                print("💡 Instala Node.js desde https://nodejs.org")
                print("   O en Linux: sudo apt install nodejs npm")
                print("⚠️ Continuando sin instalar dependencias del frontend...")
            else:
                try:
                    print("📦 Instalando dependencias del frontend...")
                    subprocess.check_call(["npm", "install"], cwd=frontend_dir)
                    print("✅ Dependencias del frontend instaladas")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Error instalando dependencias del frontend: {e}")
                    print("⚠️ Continuando sin dependencias del frontend...")
        else:
            print("ℹ️ No se detectó frontend con package.json")
        
        # Crear script de activación
        create_activation_script(python_executable)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def make_executable():
    """Hace los scripts ejecutables en Linux"""
    if platform.system() != "Windows":
        print("🔧 Configurando permisos de ejecución...")
        
        scripts = [
            "run_app.py",
            "run_app.sh",
            "run_app_wsl.py",
            "run_app_full.py",
            "build.py",
            "build_full.py",
            "test_app.py",
            "test_quick.py"
        ]
        
        for script in scripts:
            script_path = Path(__file__).parent / script
            if script_path.exists():
                os.chmod(script_path, 0o755)
                print(f"✅ {script} hecho ejecutable")

def create_activation_script(python_executable):
    """Crea un script para activar el entorno virtual"""
    print("🔧 Creando script de activación...")
    
    project_dir = Path(__file__).parent
    
    if platform.system() == "Windows":
        # Script batch para Windows
        activate_content = f'''@echo off
echo Activando entorno virtual...
call "{project_dir}\\venv\\Scripts\\activate.bat"
echo Entorno virtual activado
echo Para ejecutar la aplicación: python run_app.py
cmd /k
'''
        activate_path = project_dir / "activate.bat"
        with open(activate_path, 'w') as f:
            f.write(activate_content)
    else:
        # Script bash para Linux
        activate_content = f'''#!/bin/bash
echo "Activando entorno virtual..."
source "{project_dir}/venv/bin/activate"
echo "Entorno virtual activado"
echo "Para ejecutar la aplicación: python run_app.py"
bash
'''
        activate_path = project_dir / "activate.sh"
        with open(activate_path, 'w') as f:
            f.write(activate_content)
        os.chmod(activate_path, 0o755)
    
    print("✅ Script de activación creado")

def create_desktop_shortcut():
    """Crea un acceso directo en el escritorio"""
    print("🖥️ Creando acceso directo...")
    
    desktop = None
    if platform.system() == "Windows":
        desktop = Path.home() / "Desktop"
    else:
        desktop = Path.home() / "Desktop"
        if not desktop.exists():
            desktop = Path.home() / "Escritorio"
    
    if desktop and desktop.exists():
        if platform.system() == "Windows":
            # Crear .bat en el escritorio
            shortcut_content = f'''@echo off
cd /d "{Path(__file__).parent}"
call venv\\Scripts\\activate.bat
python run_app.py
pause
'''
            shortcut_path = desktop / "Cubo App.bat"
            with open(shortcut_path, 'w') as f:
                f.write(shortcut_content)
            print("✅ Acceso directo creado en el escritorio")
        else:
            # Crear .desktop en Linux
            shortcut_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Cubo App
Comment=Aplicación web Cubo
Exec={Path(__file__).parent}/venv/bin/python {Path(__file__).parent}/run_app.py
Icon=applications-internet
Terminal=true
Categories=Network;WebBrowser;
"""
            shortcut_path = desktop / "cubo-app.desktop"
            with open(shortcut_path, 'w') as f:
                f.write(shortcut_content)
            os.chmod(shortcut_path, 0o755)
            print("✅ Acceso directo creado en el escritorio")

def main():
    """Función principal"""
    print("🚀 Instalador de Cubo App")
    print("=" * 40)
    print()
    
    # Verificar Python
    if not check_python():
        sys.exit(1)
    
    # Verificar Node.js (opcional)
    frontend_dir = Path(__file__).parent / "frontend"
    package_json = frontend_dir / "package.json"
    
    if package_json.exists():
        print("🎨 Frontend de Vite detectado")
        if check_node_npm():
            print("✅ Node.js y npm detectados")
        else:
            print("⚠️ Node.js no detectado - el frontend no funcionará")
            print("💡 Instala Node.js desde https://nodejs.org")
            print("   O en Linux: sudo apt install nodejs npm")
        print()
    
    # Instalar dependencias
    if not install_dependencies():
        sys.exit(1)
    
    # Configurar permisos
    make_executable()
    
    # Crear acceso directo
    create_desktop_shortcut()
    
    print()
    print("🎉 ¡Instalación completada!")
    print()
    print("📋 Próximos pasos:")
    print("1. Para construir la aplicación completa: python build_full.py")
    print("2. Para ejecutar la aplicación: python run_app.py")
    print("3. Para probar: python test_quick.py")
    print()
    
    if platform.system() == "Windows":
        print("💡 En Windows también puedes:")
        print("   - Doble clic en 'run_app.bat'")
        print("   - Doble clic en 'Cubo App.bat' en el escritorio")
    else:
        print("💡 En Linux también puedes:")
        print("   - Ejecutar: ./run_app.sh")
        print("   - Doble clic en 'cubo-app.desktop' en el escritorio")

if __name__ == "__main__":
    main() 