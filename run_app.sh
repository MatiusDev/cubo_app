#!/bin/bash

echo "🚀 Iniciando Cubo App..."
echo

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 no está instalado"
    echo "💡 Por favor instala Python3: sudo apt install python3 python3-pip"
    exit 1
fi

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Error: Entorno virtual no encontrado"
    echo "💡 Ejecuta primero: python3 install.py"
    exit 1
fi

# Verificar si el script principal existe
if [ ! -f "run_app.py" ]; then
    echo "❌ Error: run_app.py no encontrado"
    exit 1
fi

# Hacer ejecutable el script si no lo es
if [ ! -x "run_app.py" ]; then
    chmod +x run_app.py
fi

# Ejecutar la aplicación
echo "🐧 Ejecutando aplicación..."
python3 run_app.py