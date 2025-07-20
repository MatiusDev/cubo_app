import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import subprocess
import threading
import time

# Importar la aplicación principal
try:
    from .main import app
except ImportError:
    # Fallback para cuando se ejecuta directamente
    import sys
    sys.path.append(str(Path(__file__).parent))
    from main import app

def get_frontend_path():
    """Obtiene la ruta al frontend"""
    # Si estamos en un ejecutable de PyInstaller
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
        return base_path / "frontend" / "dist"
    else:
        return Path(__file__).parent.parent.parent / "frontend"

def is_vite_dev_running():
    """Verifica si Vite está ejecutándose en modo desarrollo"""
    try:
        import requests
        response = requests.get("http://localhost:5173", timeout=1)
        return response.status_code == 200
    except:
        return False

def start_vite_dev():
    """Inicia Vite en modo desarrollo"""
    frontend_path = get_frontend_path()
    
    if not frontend_path.exists():
        print("❌ No se encontró el directorio frontend")
        return None
    
    try:
        # Verificar si node_modules existe
        node_modules = frontend_path / "node_modules"
        if not node_modules.exists():
            print("📦 Instalando dependencias de Vite...")
            subprocess.run(["npm", "install"], cwd=frontend_path, check=True)
            print("✅ Dependencias instaladas")
        
        # Iniciar Vite en modo desarrollo
        print("🚀 Iniciando Vite en modo desarrollo...")
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Esperar a que Vite inicie
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Vite iniciado en http://localhost:5173")
            return process
        else:
            print("❌ Error iniciando Vite")
            return None
            
    except Exception as e:
        print(f"❌ Error iniciando Vite: {e}")
        return None

def create_app():
    """Crea la aplicación FastAPI con el frontend montado"""
    # Agregar CORS para permitir comunicación con Vite
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Montar archivos estáticos del frontend
    frontend_path = get_frontend_path()
    
    # Verificar si estamos en modo desarrollo o producción
    if not getattr(sys, 'frozen', False) and frontend_path.exists():
        # Modo desarrollo: verificar si Vite está corriendo
        if is_vite_dev_running():
            print("🌐 Usando Vite en modo desarrollo (http://localhost:5173)")
        else:
            # Iniciar Vite en modo desarrollo
            vite_process = start_vite_dev()
            if vite_process:
                # Guardar el proceso para cerrarlo después
                app.state.vite_process = vite_process
    else:
        # Modo producción: servir archivos estáticos
        dist_path = frontend_path / "dist"
        if dist_path.exists():
            app.mount("/static", StaticFiles(directory=str(dist_path)), name="static")
            
            @app.get("/")
            async def serve_frontend():
                index_file = dist_path / "index.html"
                if index_file.exists():
                    return FileResponse(str(index_file))
                return {"message": "Frontend no encontrado"}
        else:
            print("⚠️ No se encontró el frontend compilado")
            print("💡 Ejecuta 'npm run build' en el directorio frontend")
    
    return app

def run_server(host="0.0.0.0", port=8000):
    """Ejecuta el servidor"""
    app_instance = create_app()
    
    try:
        uvicorn.run(app_instance, host=host, port=port)
    finally:
        # Limpiar procesos al salir
        if hasattr(app_instance.state, 'vite_process'):
            app_instance.state.vite_process.terminate()

if __name__ == "__main__":
    run_server() 