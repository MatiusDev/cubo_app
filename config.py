#!/usr/bin/env python3
"""
Clase de configuración para Cubo App
Lee variables de entorno desde config.env
"""
import os
import yaml
from typing import Optional, Dict, Any
from pathlib import Path


class Config:
    """
    Clase para manejar la configuración de la aplicación.
    Soporta archivos YAML (.yml/.yaml) y .env para compatibilidad.
    """
    
    def __init__(self, config_file: str = "config.yml"):
        """
        Inicializa la configuración desde un archivo.
        
        Args:
            config_file: Ruta al archivo de configuración (YAML o .env)
        """
        self.config_file = config_file
        self.config_data = {}
        self.load_config()
    
    def load_config(self):
        """Carga la configuración desde el archivo especificado."""
        config_path = Path(self.config_file)
        
        if not config_path.exists():
            # Intentar con archivos alternativos (compatibilidad hacia atrás)
            alternative_files = [
                "config.yaml",
                "config.env"
            ]
            
            for alt_file in alternative_files:
                if Path(alt_file).exists():
                    self.config_file = alt_file
                    config_path = Path(alt_file)
                    break
            else:
                # Crear configuración por defecto
                self.create_default_config()
                return
        
        # Determinar el tipo de archivo y cargarlo
        if config_path.suffix.lower() in ['.yml', '.yaml']:
            self._load_yaml_config(config_path)
        else:
            self._load_env_config(config_path)
    
    def _load_yaml_config(self, config_path: Path):
        """Carga configuración desde archivo YAML."""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                self.config_data = yaml.safe_load(file) or {}
            print(f"✅ Configuración cargada desde {config_path}")
        except Exception as e:
            print(f"❌ Error cargando YAML: {e}")
            self.config_data = {}
    
    def _load_env_config(self, config_path: Path):
        """Carga configuración desde archivo .env (compatibilidad)."""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Convertir valores especiales
                        if value.lower() == 'true':
                            value = True
                        elif value.lower() == 'false':
                            value = False
                        elif value.isdigit():
                            value = int(value)
                        
                        self.config_data[key] = value
            
            print(f"✅ Configuración cargada desde {config_path}")
        except Exception as e:
            print(f"❌ Error cargando .env: {e}")
            self.config_data = {}
    
    def create_default_config(self):
        """Crea una configuración por defecto en YAML."""
        default_config = {
            'mode': 'frontend',
            'backend': {
                'port': 8000,
                'host': 'localhost',
                'debug': False,
                'reload': True
            },
            'frontend': {
                'port': 5173,
                'host': 'localhost',
                'hot_reload': True,
                'open_browser': True
            },
            'build': {
                'mode': 'development',
                'clean_after_build': True,
                'pyinstaller': {
                    'onefile': True,
                    'windowed': True,
                    'icon': None
                }
            },
            'development': {
                'auto_open_browser': True,
                'debug_mode': False,
                'service_timeout': 30
            },
            'wsl': {
                'auto_detect': True,
                'use_wsl_browser': True
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file': None
            }
        }
        
        try:
            with open('config.yml', 'w', encoding='utf-8') as file:
                yaml.dump(default_config, file, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
            self.config_data = default_config
            print("✅ Configuración por defecto creada en config.yml")
        except Exception as e:
            print(f"❌ Error creando configuración por defecto: {e}")
            self.config_data = default_config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración usando notación de puntos.
        
        Args:
            key: Clave en formato 'seccion.subseccion.valor'
            default: Valor por defecto si no se encuentra
            
        Returns:
            Valor de configuración o default
        """
        keys = key.split('.')
        value = self.config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """
        Establece un valor de configuración usando notación de puntos.
        
        Args:
            key: Clave en formato 'seccion.subseccion.valor'
            value: Valor a establecer
        """
        keys = key.split('.')
        config = self.config_data
        
        # Navegar hasta la penúltima clave
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Establecer el valor
        config[keys[-1]] = value
    
    def save(self):
        """Guarda la configuración actual en el archivo."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as file:
                yaml.dump(self.config_data, file, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
            print(f"✅ Configuración guardada en {self.config_file}")
        except Exception as e:
            print(f"❌ Error guardando configuración: {e}")
    
    # Propiedades para compatibilidad con el código existente
    @property
    def mode(self) -> str:
        """Modo de operación: backend, frontend, full"""
        return self.get('mode', 'frontend')
    
    @property
    def backend_port(self) -> int:
        """Puerto del backend"""
        return self.get('backend.port', 8000)
    
    @property
    def backend_host(self) -> str:
        """Host del backend"""
        return self.get('backend.host', 'localhost')
    
    @property
    def frontend_port(self) -> int:
        """Puerto del frontend"""
        return self.get('frontend.port', 5173)
    
    @property
    def frontend_host(self) -> str:
        """Host del frontend"""
        return self.get('frontend.host', 'localhost')
    
    @property
    def build_mode(self) -> str:
        """Modo de construcción"""
        return self.get('build.mode', 'development')
    
    @property
    def clean_build(self) -> bool:
        """Limpiar después de construir"""
        return self.get('build.clean_after_build', True)
    
    @property
    def auto_open_browser(self) -> bool:
        """Abrir navegador automáticamente"""
        return self.get('development.auto_open_browser', True)
    
    @property
    def debug_mode(self) -> bool:
        """Modo debug"""
        return self.get('development.debug_mode', False)
    
    @property
    def wsl_detection(self) -> bool:
        """Detección automática de WSL"""
        return self.get('wsl.auto_detect', True)
    
    @property
    def service_timeout(self) -> int:
        """Timeout para servicios (segundos)"""
        return self.get('development.service_timeout', 30)
    
    # Métodos helper
    def is_backend_mode(self) -> bool:
        """Verifica si el modo incluye backend"""
        return self.mode in ['backend', 'full']
    
    def is_frontend_mode(self) -> bool:
        """Verifica si el modo incluye frontend"""
        return self.mode in ['frontend', 'full']
    
    def is_full_mode(self) -> bool:
        """Verifica si es modo completo"""
        return self.mode == 'full'
    
    def get_backend_url(self) -> str:
        """Obtiene la URL del backend"""
        return f"http://{self.backend_host}:{self.backend_port}"
    
    def get_frontend_url(self) -> str:
        """Obtiene la URL del frontend"""
        return f"http://{self.frontend_host}:{self.frontend_port}"
    
    def print_config(self):
        """Imprime la configuración actual de forma legible"""
        print("\n📋 Configuración Actual:")
        print("=" * 50)
        print(f"🔧 Modo: {self.mode}")
        # print(f"🌐 Backend: {self.get_backend_url()}")
        # print(f"🎨 Frontend: {self.get_frontend_url()}")
        print(f"🔨 Build Mode: {self.build_mode}")
        print(f"🐛 Debug: {self.debug_mode}")
        print(f"🌍 WSL Detection: {self.wsl_detection}")
        print("=" * 50)


# Instancia global de configuración
config = Config() 