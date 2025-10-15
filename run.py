#!/usr/bin/env python3
"""
Arquivo principal para executar a aplicação SaaS Sistema de Gestão
"""

import os
from app import app, db

if __name__ == '__main__':
    # Criar diretórios necessários
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('instance', exist_ok=True)
    
    # Criar tabelas do banco de dados se não existirem
    with app.app_context():
        db.create_all()
        print("✅ Banco de dados inicializado com sucesso!")
    
    # Executar aplicação
    print("🚀 Iniciando SaaS Sistema de Gestão...")
    print("📊 Dashboard: http://localhost:5000")
    print("👤 Login: http://localhost:5000/login")
    print("📝 Registro: http://localhost:5000/register")
    
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    )
