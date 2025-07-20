#!/usr/bin/env python3
"""
Script para construir el ejecutable de la aplicación
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

def install_pyinstaller():
    """Instala PyInstaller si no está instalado"""
    try:
        import PyInstaller
        print("PyInstaller ya está instalado")
    except ImportError:
        print("Instalando PyInstaller...")
        
        # Buscar pip del entorno virtual
        project_dir = Path(__file__).parent.parent
        venv_path = project_dir / "venv"
        
        if platform.system() == "Windows":
            pip_executable = venv_path / "Scripts" / "pip.exe"
        else:
            pip_executable = venv_path / "bin" / "pip"
        
        if pip_executable.exists():
            subprocess.check_call([str(pip_executable), "install", "pyinstaller"])
        else:
            print("❌ No se encontró el entorno virtual")
            print("💡 Ejecuta primero: python install.py")
            sys.exit(1)

def build_executable():
    """Construye el ejecutable"""
    # Obtener la ruta del directorio actual
    current_dir = Path(__file__).parent
    app_dir = current_dir / "app"
    
    # Configurar PyInstaller
    spec_file = current_dir / "cubo_app.spec"
    
    if spec_file.exists():
        # Usar archivo .spec si existe
        pyinstaller_cmd = ["pyinstaller", str(spec_file)]
    else:
        # Configuración manual
        pyinstaller_cmd = [
            "pyinstaller",
            "--onefile",  # Crear un solo archivo ejecutable
            "--console",  # Mostrar consola para debugging
            "--name", "cubo_app",  # Nombre del ejecutable
            "--add-data", f"{app_dir}:app",  # Incluir el código de la aplicación
            "--hidden-import", "uvicorn.logging",
            "--hidden-import", "uvicorn.loops",
            "--hidden-import", "uvicorn.loops.auto",
            "--hidden-import", "uvicorn.protocols",
            "--hidden-import", "uvicorn.protocols.http",
            "--hidden-import", "uvicorn.protocols.http.auto",
            "--hidden-import", "uvicorn.protocols.websockets",
            "--hidden-import", "uvicorn.protocols.websockets.auto",
            "--hidden-import", "uvicorn.lifespan",
            "--hidden-import", "uvicorn.lifespan.on",
            str(app_dir / "server.py")
        ]
    
    # Agregar archivos del frontend si existen
    frontend_dist = current_dir.parent / "frontend" / "dist"
    if frontend_dist.exists():
        pyinstaller_cmd.extend(["--add-data", f"{frontend_dist}:frontend/dist"])
    
    print("Construyendo ejecutable...")
    print(f"Comando: {' '.join(pyinstaller_cmd)}")
    
    # Ejecutar PyInstaller
    subprocess.check_call(pyinstaller_cmd, cwd=current_dir)
    
    print("¡Ejecutable construido exitosamente!")
    
    # Mostrar la ubicación del ejecutable
    dist_dir = current_dir / "dist"
    exe_name = "cubo_app.exe" if platform.system() == "Windows" else "cubo_app"
    exe_path = dist_dir / exe_name
    
    if exe_path.exists():
        print(f"Ejecutable creado en: {exe_path}")
        print(f"Tamaño: {exe_path.stat().st_size / (1024*1024):.2f} MB")
    else:
        print("Error: No se pudo encontrar el ejecutable generado")

if __name__ == "__main__":
    try:
        install_pyinstaller()
        build_executable()
    except Exception as e:
        print(f"Error durante la construcción: {e}")
        sys.exit(1) 