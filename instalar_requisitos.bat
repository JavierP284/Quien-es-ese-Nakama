@echo off
echo Verificando Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python no esta instalado. Por favor, instala Python desde https://www.python.org/downloads/
    pause
    exit /b
)

echo Instalando dependencias...
pip install --upgrade pip
pip install simpleai

echo Instalacion completa.
pause
