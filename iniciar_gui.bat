@echo off
echo 🎬 Conversor de Video - Interface Grafica
echo ==========================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nao encontrado!
    echo    Instale Python de: https://python.org
    pause
    exit /b 1
)

REM Verificar se o arquivo GUI existe
if not exist "video_converter_gui.py" (
    echo ❌ Arquivo video_converter_gui.py nao encontrado!
    pause
    exit /b 1
)

REM Tentar iniciar a GUI
echo 🚀 Iniciando interface grafica...
python video_converter_gui.py

REM Se houver erro, mostrar mensagem
if errorlevel 1 (
    echo.
    echo ❌ Erro ao iniciar a GUI!
    echo    Execute: python install_gui_dependencies.py
    pause
)