#!/usr/bin/env python3
"""
Script para configurar la aplicación Cubo App.
Crea archivos de configuración YAML de forma interactiva o por argumentos.
"""

import sys
import yaml
from pathlib import Path


def create_yaml_config(mode: str = "frontend", interactive: bool = False):
    """
    Crea un archivo de configuración YAML.
    
    Args:
        mode: Modo de configuración (backend, frontend, full)
        interactive: Si es True, solicita valores al usuario
    """
    
    if interactive:
        print("🔧 Configuración Interactiva de Cubo App")
        print("=" * 50)
        
        # Modo
        print("\n📋 Selecciona el modo de operación:")
        print("1. backend - Solo servidor backend")
        print("2. frontend - Solo aplicación frontend (recomendado)")
        print("3. full - Backend + Frontend")
        
        while True:
            choice = input("\nSelecciona (1-3) [2]: ").strip() or "2"
            if choice == "1":
                mode = "backend"
                break
            elif choice == "2":
                mode = "frontend"
                break
            elif choice == "3":
                mode = "full"
                break
            else:
                print("❌ Opción inválida. Selecciona 1, 2 o 3.")
        
        # Configuración del backend
        if mode in ["backend", "full"]:
            print(f"\n🌐 Configuración del Backend:")
            backend_port = input("Puerto del backend [8000]: ").strip() or "8000"
            backend_host = input("Host del backend [localhost]: ").strip() or "localhost"
            backend_debug = input("Modo debug (y/n) [n]: ").strip().lower() or "n"
            backend_reload = input("Auto-reload (y/n) [y]: ").strip().lower() or "y"
        else:
            backend_port = "8000"
            backend_host = "localhost"
            backend_debug = "n"
            backend_reload = "y"
        
        # Configuración del frontend
        if mode in ["frontend", "full"]:
            print(f"\n🎨 Configuración del Frontend:")
            frontend_port = input("Puerto del frontend [5173]: ").strip() or "5173"
            frontend_host = input("Host del frontend [localhost]: ").strip() or "localhost"
            frontend_hot_reload = input("Hot reload (y/n) [y]: ").strip().lower() or "y"
            frontend_open_browser = input("Abrir navegador automáticamente (y/n) [y]: ").strip().lower() or "y"
        else:
            frontend_port = "5173"
            frontend_host = "localhost"
            frontend_hot_reload = "y"
            frontend_open_browser = "y"
        
        # Configuración de desarrollo
        print(f"\n🔧 Configuración de Desarrollo:")
        auto_open_browser = input("Abrir navegador automáticamente (y/n) [y]: ").strip().lower() or "y"
        debug_mode = input("Modo debug (y/n) [n]: ").strip().lower() or "n"
        service_timeout = input("Timeout de servicios (segundos) [30]: ").strip() or "30"
        
        # Configuración de construcción
        print(f"\n🔨 Configuración de Construcción:")
        build_mode = input("Modo de construcción (development/production) [development]: ").strip() or "development"
        clean_build = input("Limpiar después de construir (y/n) [y]: ").strip().lower() or "y"
        
        # Configuración de WSL
        print(f"\n🌍 Configuración de WSL:")
        wsl_auto_detect = input("Detección automática de WSL (y/n) [y]: ").strip().lower() or "y"
        wsl_use_browser = input("Usar navegador WSL (y/n) [y]: ").strip().lower() or "y"
        
        # Configuración de logs
        print(f"\n📝 Configuración de Logs:")
        log_level = input("Nivel de log (DEBUG/INFO/WARNING/ERROR) [INFO]: ").strip() or "INFO"
        
    else:
        # Valores por defecto
        backend_port = "8000"
        backend_host = "localhost"
        backend_debug = "n"
        backend_reload = "y"
        frontend_port = "5173"
        frontend_host = "localhost"
        frontend_hot_reload = "y"
        frontend_open_browser = "y"
        auto_open_browser = "y"
        debug_mode = "n"
        service_timeout = "30"
        build_mode = "development"
        clean_build = "y"
        wsl_auto_detect = "y"
        wsl_use_browser = "y"
        log_level = "INFO"
    
    # Convertir valores booleanos
    def to_bool(value: str) -> bool:
        return value.lower() in ['y', 'yes', 'true', '1']
    
    def to_int(value: str) -> int:
        try:
            return int(value)
        except ValueError:
            return 30
    
    # Crear configuración
    config = {
        'mode': mode,
        'backend': {
            'port': to_int(backend_port),
            'host': backend_host,
            'debug': to_bool(backend_debug),
            'reload': to_bool(backend_reload)
        },
        'frontend': {
            'port': to_int(frontend_port),
            'host': frontend_host,
            'hot_reload': to_bool(frontend_hot_reload),
            'open_browser': to_bool(frontend_open_browser)
        },
        'build': {
            'mode': build_mode,
            'clean_after_build': to_bool(clean_build),
            'pyinstaller': {
                'onefile': True,
                'windowed': True,
                'icon': None
            }
        },
        'development': {
            'auto_open_browser': to_bool(auto_open_browser),
            'debug_mode': to_bool(debug_mode),
            'service_timeout': to_int(service_timeout)
        },
        'wsl': {
            'auto_detect': to_bool(wsl_auto_detect),
            'use_wsl_browser': to_bool(wsl_use_browser)
        },
        'logging': {
            'level': log_level,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'file': None
        }
    }
    
    # Guardar configuración
    config_file = "config.yml"
    
    try:
        with open(config_file, 'w', encoding='utf-8') as file:
            yaml.dump(config, file, default_flow_style=False, 
                     allow_unicode=True, sort_keys=False)
        
        print(f"\n✅ Configuración guardada en {config_file}")
        print(f"🔧 Modo configurado: {mode}")
        
        if mode == "backend":
            print(f"🌐 Backend: http://{backend_host}:{backend_port}")
        elif mode == "frontend":
            print(f"🎨 Frontend: http://{frontend_host}:{frontend_port}")
        else:
            print(f"🌐 Backend: http://{backend_host}:{backend_port}")
            print(f"🎨 Frontend: http://{frontend_host}:{frontend_port}")
        
        print(f"\n💡 Para ejecutar: python3 run_app.py")
        print(f"💡 Para construir: python3 build.py")
        
    except Exception as e:
        print(f"❌ Error guardando configuración: {e}")
        return False
    
    return True


def main():
    """Función principal"""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode not in ['backend', 'frontend', 'full']:
            print("❌ Modo inválido. Usa: backend, frontend, o full")
            print("💡 Ejemplo: python3 configure.py frontend")
            return False
        
        print(f"🔧 Configurando modo: {mode}")
        return create_yaml_config(mode, interactive=False)
    else:
        # Sin argumentos, usar frontend por defecto
        print("🔧 Configurando modo: frontend (por defecto)")
        return create_yaml_config("frontend", interactive=False)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 