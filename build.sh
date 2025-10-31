#!/bin/bash

# Script de build para Render
echo "🔧 Iniciando build para Render..."

# Limpar cache do pip
echo "🧹 Limpando cache do pip..."
pip cache purge

# Instalar dependências sem cache
echo "📦 Instalando dependências..."
pip install --no-cache-dir -r requirements_render.txt

# Verificar instalação
echo "✅ Verificando instalação..."
python -c "import flask; print('Flask instalado com sucesso')"
python -c "import psycopg2; print('PostgreSQL driver instalado com sucesso')"

# Corrigir banco de dados se necessário
echo "🔧 Verificando banco de dados..."
python -c "
import os
from app import app, db
with app.app_context():
    try:
        from app import User
        User.query.first()
        print('✅ Banco de dados OK!')
    except Exception as e:
        print(f'⚠️ Problema no banco: {e}')
        print('🔄 Recriando schema...')
        db.drop_all()
        db.create_all()
        print('✅ Schema recriado!')
"

# Executar migração de código de barras se necessário
echo "🔧 Verificando migração codigo_barras..."
python add_codigo_barras_render.py

echo "🎉 Build concluído!"
