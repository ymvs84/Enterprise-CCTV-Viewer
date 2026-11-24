@echo off
setlocal
title Servidor VUS - JCDecaux
cd /d "%~dp0"
cls

echo =====================================================================
echo             JCDecaux - Visor Unificado de Seguridad (VUS)
echo                     Script de Arranque Automatico
echo =====================================================================
echo.

echo [1/3] Levantando Servidor de Video (MediaMTX)...
if not exist "MediaServer\mediamtx.exe" goto mediamtx_missing
tasklist /FI "IMAGENAME eq mediamtx.exe" | find /I "mediamtx.exe" >nul
if not errorlevel 1 goto mediamtx_ready
start "" /B "%~dp0MediaServer\mediamtx.exe" "%~dp0MediaServer\mediamtx.yml"
echo [OK] Servidor multimedia activo en segundo plano.
goto python_setup

:mediamtx_ready
echo [INFO] MediaMTX ya estaba activo.
goto python_setup

:mediamtx_missing
echo [ERROR CRITICO] No se encontro MediaServer\mediamtx.exe
goto error

:python_setup
echo.
echo [2/3] Comprobando entorno de ejecucion Python...
set "PYTHON=%~dp0.venv\Scripts\python.exe"
set "NEEDS_SETUP=0"
if exist "%PYTHON%" goto python_ready

echo [ALERTA] Entorno virtual no detectado. Creando entorno...
set "NEEDS_SETUP=1"
where python >nul 2>&1
if errorlevel 1 goto python_missing
python -m venv "%~dp0.venv"
if errorlevel 1 goto python_setup_failed
set "PYTHON=%~dp0.venv\Scripts\python.exe"

echo [INFO] Instalando librerias del proyecto...
"%PYTHON%" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 goto dependencies_failed

:python_ready
echo [INFO] Entorno Python valido detectado.
echo [INFO] Aplicando migraciones de base de datos...
"%PYTHON%" "%~dp0manage.py" migrate
if errorlevel 1 goto database_failed

if "%NEEDS_SETUP%"=="0" goto web_setup
echo [INFO] Cargando inventario de camaras...
"%PYTHON%" "%~dp0manage.py" cargar_camaras
if errorlevel 1 goto database_failed
goto web_setup

:python_missing
echo [ERROR CRITICO] Python no esta instalado o no esta disponible en PATH.
goto error

:python_setup_failed
echo [ERROR CRITICO] No se pudo crear el entorno virtual.
goto error

:dependencies_failed
echo [ERROR CRITICO] No se pudieron instalar las dependencias.
goto error

:database_failed
echo [ERROR CRITICO] No se pudo preparar la base de datos.
goto error

:web_setup
echo.
echo [3/3] Abriendo Visor de Seguridad en Modo App...
start "" /B "%PYTHON%" "%~dp0manage.py" runserver 127.0.0.1:8000 --noreload
timeout /t 3 /nobreak >nul
start "" msedge.exe --app=http://127.0.0.1:8000

echo.
echo ===================================================
echo     SISTEMA ACTIVO Y CORRIENDO EN SEGUNDO PLANO
echo ===================================================
echo.
exit /b 0

:error
echo.
echo El arranque no se ha completado. Revisa el error anterior.
pause
exit /b 1
