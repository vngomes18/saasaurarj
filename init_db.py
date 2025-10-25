#!/usr/bin/env python3
"""
Script de inicialização do banco de dados para Render
"""

import os
import sys
from app import app, db, User

def init_database():
    """Inicializa o banco de dados e cria tabelas"""
    print("🔧 Inicializando banco de dados...")
    
    with app.app_context():
        try:
            # Criar todas as tabelas
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
            
            # Verificar se já existe um usuário admin
            admin_user = User.query.filter_by(email='arthurnavarro160203@gmail.com').first()
            
            if not admin_user:
                print("👤 Criando usuário administrador...")
                admin_user = User(
                    email='arthurnavarro160203@gmail.com',
                    password='admin123',  # Senha padrão - deve ser alterada
                    role='admin',
                    nome='Administrador',
                    ativo=True
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Usuário administrador criado!")
                print("📧 Email: arthurnavarro160203@gmail.com")
                print("🔑 Senha: admin123")
                print("⚠️  IMPORTANTE: Altere a senha após o primeiro login!")
            else:
                print("✅ Usuário administrador já existe!")
            
            print("🎉 Banco de dados inicializado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar banco de dados: {e}")
            sys.exit(1)

if __name__ == '__main__':
    init_database()
