@echo off
chcp 65001 >nul
echo 🚀 Iniciando Cubo App...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo 💡 Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

REM Ejecutar la aplicación
python run_app.py

pause 