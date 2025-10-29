#!/bin/bash

echo "========================================"
echo "   BUILD REACT PARA PRODUÇÃO"
echo "========================================"
echo

echo "[1/3] Instalando dependências..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao instalar dependências"
    exit 1
fi

echo
echo "[2/3] Criando build de produção..."
npm run build
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao criar build"
    exit 1
fi

echo
echo "[3/3] Build criado com sucesso!"
echo
echo "========================================"
echo "  BUILD REACT CONCLUÍDO!"
echo "========================================"
echo
echo "Arquivos gerados em: frontend/dist/"
echo
echo "Para servir o build:"
echo "  cd frontend"
echo "  npm run serve"
echo
