@echo off
echo ========================================
echo    SAAS SISTEMA - APENAS REACT
echo ========================================
echo.

echo [1/4] Instalando dependencias do React...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo [2/4] Iniciando servidor Flask (API Backend)...
start "Flask API" cmd /k "cd .. && python run.py"

echo.
echo [3/4] Aguardando Flask inicializar...
timeout /t 5 /nobreak > nul

echo [4/4] Iniciando React Frontend...
echo.
echo ========================================
echo   SISTEMA REACT INICIADO!
echo ========================================
echo.
echo API Backend:  http://localhost:5000/api
echo Frontend:     http://localhost:3000
echo.
echo O Flask agora serve APENAS a API
echo O React é o frontend principal
echo.
echo Pressione Ctrl+C para parar
echo.

call npm run dev
