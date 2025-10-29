#!/bin/bash

echo "========================================"
echo "   INICIANDO SAAS SISTEMA - REACT"
echo "========================================"
echo

echo "[1/3] Instalando dependências do React..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao instalar dependências"
    exit 1
fi

echo
echo "[2/3] Iniciando servidor Flask (Backend)..."
cd ..
python run.py &
FLASK_PID=$!

echo
echo "[3/3] Aguardando Flask inicializar..."
sleep 5

echo "Iniciando React Frontend..."
echo
echo "========================================"
echo "  SISTEMA INICIADO COM SUCESSO!"
echo "========================================"
echo
echo "Backend Flask:  http://localhost:5000"
echo "Frontend React: http://localhost:3000"
echo
echo "Pressione Ctrl+C para parar ambos os servidores"
echo

cd frontend
npm run dev

# Limpar processo Flask quando sair
trap "kill $FLASK_PID" EXIT
