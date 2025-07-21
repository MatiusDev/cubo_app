import subprocess
import sys
import os
import webbrowser
import tkinter.messagebox as mbox
from pathlib import Path

def main():
    try:
        frontend_dir = Path(__file__).parent / "frontend"
        if not (frontend_dir / "package.json").exists():
            mbox.showerror("Cubo App Frontend", "No se encontró el frontend (package.json)")
            sys.exit(1)

        # Instalar dependencias si no existen
        if not (frontend_dir / "node_modules").exists():
            mbox.showinfo("Cubo App Frontend", "Instalando dependencias de frontend...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)

        # Lanzar Vite
        proc = subprocess.Popen(["npm", "run", "dev"], cwd=frontend_dir)
        webbrowser.open("http://localhost:5173")
        mbox.showinfo("Cubo App Frontend", "El frontend está corriendo en http://localhost:5173\nCierra esta ventana para detener el proceso.")
        proc.wait()
    except Exception as e:
        mbox.showerror("Cubo App Frontend", f"Error al ejecutar el frontend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 