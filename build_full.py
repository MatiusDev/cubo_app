#!/usr/bin/env python3
"""
Script para construir la aplicación completa (Backend + Frontend Vite)
"""
import os
import sys
import platform
import subprocess
from pathlib import Path

def check_node_npm():
    """Verifica que Node.js y npm estén instalados"""
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def build_frontend():
    """Construye el frontend con Vite"""
    print("🎨 Construyendo frontend con Vite...")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print("❌ No se encontró el directorio frontend")
        return False
    
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ No se encontró package.json en el frontend")
        return False
    
    try:
        # Verificar dependencias
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print("📦 Instalando dependencias del frontend...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            print("✅ Dependencias instaladas")
        
        # Construir el frontend
        print("🔨 Construyendo frontend...")
        subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True)
        print("✅ Frontend construido")
        
        # Verificar que se creó la carpeta dist
        dist_path = frontend_dir / "dist"
        if dist_path.exists():
            print(f"📁 Frontend compilado en: {dist_path}")
            return True
        else:
            print("❌ No se encontró la carpeta dist después del build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error construyendo frontend: {e}")
        return False

def build_backend():
    """Construye el backend con PyInstaller"""
    print("🔧 Construyendo backend...")
    
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
    
    # Ejecutar el script de construcción del backend
    build_script = Path(__file__).parent / "backend" / "build_exe.py"
    
    if build_script.exists():
        try:
            subprocess.check_call([sys.executable, str(build_script)])
            print("✅ Backend construido exitosamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error construyendo backend: {e}")
            return False
    else:
        print("❌ No se encontró el script de construcción del backend")
        return False

def create_launcher():
    """Crea un launcher que use el frontend compilado"""
    print("🎯 Creando launcher...")
    
    project_dir = Path(__file__).parent
    
    # Crear un launcher que use el frontend compilado
    launcher_content = '''#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

# Ejecutar el script principal
script_path = Path(__file__).parent / "run_app.py"
subprocess.run([sys.executable, str(script_path)])
'''
    
    launcher_path = project_dir / "launcher.py"
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    # Hacer ejecutable en Linux
    if platform.system() != "Windows":
        os.chmod(launcher_path, 0o755)
    
    print("✅ Launcher creado")

def main():
    """Función principal"""
    print("🚀 Construyendo Cubo App Completa")
    print("=" * 40)
    print()
    
    # Verificar Node.js y npm
    if not check_node_npm():
        print("❌ Error: Node.js y npm no están instalados")
        print("💡 Instala Node.js desde https://nodejs.org")
        sys.exit(1)
    
    # Construir frontend
    if not build_frontend():
        print("❌ Error construyendo frontend")
        sys.exit(1)
    
    # Construir backend
    if not build_backend():
        print("❌ Error construyendo backend")
        sys.exit(1)
    
    # Crear launcher
    create_launcher()
    
    print()
    print("🎉 ¡Construcción completada!")
    print()
    print("📁 Archivos generados:")
    print("   - backend/dist/cubo_app (Linux) o cubo_app.exe (Windows)")
    print("   - frontend/dist/ (Frontend compilado)")
    print("   - run_app.py (script principal)")
    print("   - run_app_full.py (script completo)")
    print("   - launcher.py (launcher simple)")
    print()
    print("🚀 Para ejecutar la aplicación:")
    if platform.system() == "Windows":
        print("   - Doble clic en 'run_app.bat'")
        print("   - O ejecuta: python run_app.py")
    else:
        print("   - Ejecuta: ./run_app.sh")
        print("   - O ejecuta: python3 run_app.py")
    print()
    print("💡 La aplicación ahora usará el frontend compilado en modo producción")

if __name__ == "__main__":
    main() 