@echo off
echo ========================================
echo    INICIANDO SAAS SISTEMA - REACT
echo ========================================
echo.

echo [1/3] Instalando dependencias do React...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo [2/3] Iniciando servidor Flask (Backend)...
start "Flask Backend" cmd /k "cd .. && python run.py"

echo.
echo [3/3] Aguardando Flask inicializar...
timeout /t 5 /nobreak > nul

echo Iniciando React Frontend...
echo.
echo ========================================
echo   SISTEMA INICIADO COM SUCESSO!
echo ========================================
echo.
echo Backend Flask:  http://localhost:5000
echo Frontend React: http://localhost:3000
echo.
echo Pressione Ctrl+C para parar ambos os servidores
echo.

call npm run dev
