import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# Importar la aplicación principal
try:
    from .main import app
except ImportError:
    import sys
    sys.path.append(str(Path(__file__).parent))
    from main import app

def get_frontend_dist_path():
    """Obtiene la ruta al frontend compilado (dist)"""
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
        return base_path / "frontend" / "dist"
    else:
        return Path(__file__).parent.parent.parent / "frontend" / "dist"

def create_app():
    """Crea la aplicación FastAPI y monta el frontend solo en producción si existe."""
    # Agregar CORS para permitir comunicación con el frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Montar archivos estáticos del frontend solo si existe el build
    dist_path = get_frontend_dist_path()
    if dist_path.exists():
        app.mount("/static", StaticFiles(directory=str(dist_path)), name="static")
        @app.get("/")
        async def serve_frontend():
            index_file = dist_path / "index.html"
            if index_file.exists():
                return FileResponse(str(index_file))
            return {"message": "Frontend no encontrado"}
    else:
        print("⚠️ No se encontró el frontend compilado (dist)")
        print("💡 Ejecuta 'npm run build' en el directorio frontend si quieres servir el frontend en producción")
    return app

def run_server(host="0.0.0.0", port=8000):
    """Ejecuta el servidor FastAPI"""
    app_instance = create_app()
    uvicorn.run(app_instance, host=host, port=port)

if __name__ == "__main__":
    run_server() 