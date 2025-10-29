@echo off
echo ========================================
echo    BUILD REACT PARA PRODUÇÃO
echo ========================================
echo.

echo [1/3] Instalando dependencias...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo [2/3] Criando build de produção...
call npm run build
if %errorlevel% neq 0 (
    echo ERRO: Falha ao criar build
    pause
    exit /b 1
)

echo.
echo [3/3] Build criado com sucesso!
echo.
echo ========================================
echo   BUILD REACT CONCLUÍDO!
echo ========================================
echo.
echo Arquivos gerados em: frontend/dist/
echo.
echo Para servir o build:
echo   cd frontend
echo   npm run serve
echo.
pause
