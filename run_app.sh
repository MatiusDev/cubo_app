#!/bin/bash

echo "🚀 Iniciando Cubo App..."
echo

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 no está instalado"
    echo "💡 Por favor instala Python3: sudo apt install python3 python3-pip"
    exit 1
fi

# Verificar si estamos en WSL2
if grep -qi microsoft /proc/version 2>/dev/null; then
    echo "🐧 WSL2 detectado, usando script específico..."
    chmod +x run_app_wsl.py
    python3 run_app_wsl.py
else
    echo "🐧 Linux nativo detectado..."
    chmod +x run_app.py
    python3 run_app.py
fi 