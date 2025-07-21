import subprocess
import sys
import shutil
import tkinter.messagebox as mbox


def is_installed(cmd):
    return shutil.which(cmd) is not None


def main():
    # Verificar Python
    if not is_installed('python') and not is_installed('python3'):
        mbox.showerror("Cubo App Setup", "Python no está instalado.\nPor favor instala Python desde https://python.org antes de continuar.")
        sys.exit(1)

    # Verificar Node.js
    if not is_installed('node') or not is_installed('npm'):
        mbox.showerror("Cubo App Setup", "Node.js y npm no están instalados.\nPor favor instala Node.js desde https://nodejs.org antes de continuar.")
        sys.exit(1)

    # Ejecutar install.py
    try:
        result = subprocess.run([sys.executable, "install.py"], check=True)
        mbox.showinfo("Cubo App Setup", "¡Setup completado exitosamente!")
    except subprocess.CalledProcessError as e:
        mbox.showerror("Cubo App Setup", f"Error durante el setup.\nRevisa la consola para más detalles.")
        sys.exit(1)
    except Exception as e:
        mbox.showerror("Cubo App Setup", f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 