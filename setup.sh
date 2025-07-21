#!/bin/bash

echo "🚀 Setup de Cubo App"
echo "===================="
echo

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 no está instalado"
    echo "💡 Por favor instala Python3: sudo apt install python3 python3-pip"
    exit 1
fi

# Verificar si el script install.py existe
if [ ! -f "install.py" ]; then
    echo "❌ Error: install.py no encontrado"
    echo "💡 Asegúrate de estar en el directorio correcto del proyecto"
    exit 1
fi

# Verificar si existe configuración
if [ ! -f "config.yml" ]; then
    echo "⚠️ No se encontró config.yml"
    echo "💡 Creando configuración por defecto..."
    python3 configure.py backend
fi

# Hacer ejecutable install.py si no lo es
if [ ! -x "install.py" ]; then
    chmod +x install.py
    echo "✅ Permisos de ejecución configurados para install.py"
fi

# Ejecutar install.py
echo "🔧 Ejecutando instalación..."
echo

if python3 install.py; then
    echo
    echo "🎉 ¡Setup completado exitosamente!"
    echo
    echo "📋 Próximos pasos:"
    echo "1. Para ejecutar la aplicación: ./run_app.sh"
    echo "2. Para construir la aplicación: python3 build.py"
    echo "3. Para probar: python3 test_quick.py"
    echo
    echo "💡 También puedes ejecutar directamente:"
    echo "   python3 run_app.py"
else
    echo
    echo "❌ Error durante el setup"
    echo "💡 Revisa los errores anteriores e intenta nuevamente"
    exit 1
fi 