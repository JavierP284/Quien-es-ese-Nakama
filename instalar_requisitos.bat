@echo off
setlocal

:: ===== Verificar Python =====
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python no esta instalado. Se descargara e instalara automaticamente...
    
    :: Descargar instalador de Python (ejemplo 3.11.9) usando powershell
    set PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
    set PYTHON_INSTALLER=%TEMP%\python_installer.exe

    echo Descargando Python...
    powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'"
    
    echo Instalando Python silenciosamente...
    "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    if %ERRORLEVEL% NEQ 0 (
        echo Error durante la instalacion de Python.
        pause
        exit /b
    )
    
    echo Instalacion de Python completa.
)

:: ===== Instalar dependencias =====
echo Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install simpleai

echo Instalacion completa.
pause
