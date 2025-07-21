#!/usr/bin/env python3
"""
Script unificado para construir Cubo App
Controlado por config.env
"""
import os
import sys
import platform
import subprocess
from pathlib import Path

# Importar configuración
from config import config

def check_node_npm():
    """Verifica que Node.js y npm estén instalados"""
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True, timeout=10)
        subprocess.run(["npm", "--version"], check=True, capture_output=True, timeout=10)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False

def install_dependencies():
    """Instala las dependencias necesarias según configuración"""
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
    
    # Instalar dependencias del backend si está habilitado
    if config.is_backend_mode():
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
        
        # Instalar PyInstaller para backend
        try:
            subprocess.check_call([
                str(pip_executable), "install", "pyinstaller"
            ])
            print("✅ PyInstaller instalado")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando PyInstaller: {e}")
            return False
    
    # Instalar dependencias del frontend si está habilitado
    if config.is_frontend_mode():
        if not check_node_npm():
            print("❌ Error: Node.js y npm no están instalados")
            print("💡 Instala Node.js desde https://nodejs.org")
            return False
        
        frontend_dir = Path(__file__).parent / "frontend"
        if frontend_dir.exists():
            node_modules = frontend_dir / "node_modules"
            if not node_modules.exists():
                print("📦 Instalando dependencias del frontend...")
                try:
                    subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, timeout=300)
                    print("✅ Dependencias del frontend instaladas")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Error instalando dependencias del frontend: {e}")
                    return False
                except subprocess.TimeoutExpired:
                    print("❌ Timeout instalando dependencias del frontend")
                    return False
    
    return True

def build_frontend():
    """Construye el frontend con Vite"""
    if not config.is_frontend_mode():
        config.log("Modo frontend no habilitado")
        return True
    
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
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, timeout=300)
            print("✅ Dependencias instaladas")
        
        # Construir el frontend
        print("🔨 Construyendo frontend...")
        subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True, timeout=300)
        print("✅ Frontend construido")
        
        # Verificar que se creó la carpeta dist
        dist_path = frontend_dir / "dist"
        if dist_path.exists():
            # Verificar que hay archivos en dist
            files = list(dist_path.rglob("*"))
            if files:
                print(f"📁 Frontend compilado en: {dist_path}")
                print(f"📄 Archivos generados: {len(files)}")
                return True
            else:
                print("❌ La carpeta dist está vacía")
                return False
        else:
            print("❌ No se encontró la carpeta dist después del build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error construyendo frontend: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Timeout construyendo frontend")
        return False

def build_backend():
    """Construye el backend con PyInstaller"""
    if not config.is_backend_mode():
        config.log("Modo backend no habilitado")
        return True
    
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
            subprocess.check_call([sys.executable, str(build_script)], timeout=600)
            print("✅ Backend construido exitosamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error construyendo backend: {e}")
            return False
        except subprocess.TimeoutExpired:
            print("❌ Timeout construyendo backend")
            return False
    else:
        print("❌ No se encontró el script de construcción del backend")
        print(f"💡 Buscando en: {build_script}")
        return False

def validate_output():
    """Valida que los archivos necesarios se hayan creado"""
    print("🔍 Validando archivos de salida...")
    
    current_dir = Path(__file__).parent
    backend_dir = current_dir / "backend"
    frontend_dir = current_dir / "frontend"
    
    # Verificar frontend compilado si está habilitado
    if config.is_frontend_mode():
        frontend_dist = frontend_dir / "dist"
        if not frontend_dist.exists():
            print("❌ No se encontró frontend/dist")
            return False
        
        frontend_files = list(frontend_dist.rglob("*"))
        if not frontend_files:
            print("❌ Frontend/dist está vacío")
            return False
        
        print(f"✅ Frontend compilado: {len(frontend_files)} archivos")
    
    # Verificar backend ejecutable si está habilitado
    if config.is_backend_mode():
        if platform.system() == "Windows":
            exe_name = "cubo_app.exe"
        else:
            exe_name = "cubo_app"
        
        possible_paths = [
            backend_dir / "dist" / exe_name,
            current_dir / "dist" / exe_name,
            current_dir / exe_name,
            backend_dir / exe_name
        ]
        
        backend_found = False
        for path in possible_paths:
            if path.exists():
                if platform.system() != "Windows":
                    if not os.access(path, os.X_OK):
                        try:
                            os.chmod(path, 0o755)
                            print(f"✅ Permisos de ejecución configurados para: {path}")
                        except Exception as e:
                            print(f"⚠️ No se pudieron configurar permisos para: {path}")
                
                print(f"✅ Backend ejecutable encontrado: {path}")
                print(f"📏 Tamaño: {path.stat().st_size / (1024*1024):.1f} MB")
                backend_found = True
                break
        
        if not backend_found:
            print("❌ No se encontró el ejecutable del backend")
            return False
    
    return True

def create_launcher():
    """Crea un launcher según la configuración"""
    print("🎯 Creando launcher...")
    
    project_dir = Path(__file__).parent
    
    # Crear un launcher que use el script unificado
    launcher_content = '''#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

# Ejecutar el script principal unificado
script_path = Path(__file__).parent / "run_app_new.py"
subprocess.run([sys.executable, str(script_path)])
'''
    
    launcher_path = project_dir / "launcher.py"
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    # Hacer ejecutable en Linux
    if platform.system() != "Windows":
        os.chmod(launcher_path, 0o755)
    
    print("✅ Launcher creado")

def cleanup_temp_files():
    """Limpia archivos temporales de construcción"""
    if not config.clean_build:
        config.log("Clean build deshabilitado")
        return
        
    print("🧹 Limpiando archivos temporales...")
    
    current_dir = Path(__file__).parent
    temp_dirs = [
        current_dir / "build",
        current_dir / "__pycache__",
        current_dir / "backend" / "build",
        current_dir / "backend" / "__pycache__"
    ]
    
    # Agregar directorios del frontend si está habilitado
    if config.is_frontend_mode():
        temp_dirs.extend([
            current_dir / "frontend" / "node_modules" / ".cache",
            current_dir / "frontend" / ".vite"
        ])
    
    for temp_dir in temp_dirs:
        if temp_dir.exists():
            try:
                import shutil
                shutil.rmtree(temp_dir)
                print(f"✅ Limpiado: {temp_dir}")
            except Exception as e:
                print(f"⚠️ No se pudo limpiar {temp_dir}: {e}")

def main():
    """Función principal"""
    print("🚀 Construyendo Cubo App (Unificado)")
    print("=" * 40)
    print()
    
    # Mostrar configuración
    config.print_config()
    
    # Verificar Node.js si se necesita frontend
    if config.is_frontend_mode():
        if not check_node_npm():
            print("❌ Error: Node.js y npm no están instalados")
            print("💡 Instala Node.js desde https://nodejs.org")
            sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        print("❌ Error instalando dependencias")
        sys.exit(1)
    
    # Construir frontend si está habilitado
    if config.is_frontend_mode():
        if not build_frontend():
            print("❌ Error construyendo frontend")
            sys.exit(1)
    
    # Construir backend si está habilitado
    if config.is_backend_mode():
        if not build_backend():
            print("❌ Error construyendo backend")
            sys.exit(1)
    
    # Validar salida
    if not validate_output():
        print("❌ Error validando archivos de salida")
        sys.exit(1)
    
    # Crear launcher
    create_launcher()
    
    # Limpiar archivos temporales
    cleanup_temp_files()
    
    print()
    print("🎉 ¡Construcción completada!")
    print()
    print("📁 Archivos generados:")
    if config.is_backend_mode():
        print("   - backend/dist/cubo_app (Linux) o cubo_app.exe (Windows)")
    if config.is_frontend_mode():
        print("   - frontend/dist/ (Frontend compilado)")
    print("   - run_app_new.py (script unificado)")
    print("   - launcher.py (launcher simple)")
    print()
    print("🚀 Para ejecutar la aplicación:")
    print("   python run_app_new.py")
    print("   o ./launcher.py")

if __name__ == "__main__":
    main() 