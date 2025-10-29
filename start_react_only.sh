#!/bin/bash

echo "========================================"
echo "   SAAS SISTEMA - APENAS REACT"
echo "========================================"
echo

echo "[1/4] Instalando dependências do React..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao instalar dependências"
    exit 1
fi

echo
echo "[2/4] Iniciando servidor Flask (API Backend)..."
cd ..
python run.py &
FLASK_PID=$!

echo
echo "[3/4] Aguardando Flask inicializar..."
sleep 5

echo "[4/4] Iniciando React Frontend..."
echo
echo "========================================"
echo "  SISTEMA REACT INICIADO!"
echo "========================================"
echo
echo "API Backend:  http://localhost:5000/api"
echo "Frontend:     http://localhost:3000"
echo
echo "O Flask agora serve APENAS a API"
echo "O React é o frontend principal"
echo
echo "Pressione Ctrl+C para parar"
echo

cd frontend
npm run dev

# Limpar processo Flask quando sair
trap "kill $FLASK_PID" EXIT
