import subprocess
import sys
import os
import webbrowser
import tkinter.messagebox as mbox
from pathlib import Path

def main():
    try:
        venv_python = Path("venv/Scripts/python.exe")
        if not venv_python.exists():
            mbox.showerror("Cubo App Backend", "No se encontró el entorno virtual. Ejecuta el setup primero.")
            sys.exit(1)
        proc = subprocess.Popen([str(venv_python), "run_app.py"])
        webbrowser.open("http://localhost:8000")
        mbox.showinfo("Cubo App Backend", "El backend está corriendo en http://localhost:8000\nCierra esta ventana para detener el proceso.")
        proc.wait()
    except Exception as e:
        mbox.showerror("Cubo App Backend", f"Error al ejecutar el backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 