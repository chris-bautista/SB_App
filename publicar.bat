@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================
echo   Publicar cambios de Auto Servicio Bautista
echo ============================================
echo.

echo [1/4] Regenerando docs/ con el contenido actual de contenido.py...
".venv\Scripts\python.exe" exportar_estatico.py
if errorlevel 1 (
    echo.
    echo ERROR: no se pudo generar docs/. Revisa el mensaje de arriba.
    echo Es probable que contenido.py tenga un error de sintaxis.
    pause
    exit /b 1
)

echo.
echo [2/4] Preparando cambios para Git...
git add -A

set MSG=
set /p MSG="Describe brevemente el cambio (Enter para usar 'Actualizar sitio'): "
if "%MSG%"=="" set MSG=Actualizar sitio

echo.
echo [3/4] Creando commit...
git commit -m "%MSG%"
if errorlevel 1 (
    echo No habia cambios nuevos que guardar. Se intentara subir de todos modos,
    echo por si quedo algun commit pendiente de una vez anterior.
)

echo.
echo [4/4] Subiendo a GitHub...
git push
if errorlevel 1 (
    echo.
    echo ERROR: el push fallo. Revisa tu conexion a internet o si necesitas
    echo volver a iniciar sesion en GitHub.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Listo! En 1-2 minutos se actualiza:
echo   https://chris-bautista.github.io/SB_App/
echo ============================================
pause
