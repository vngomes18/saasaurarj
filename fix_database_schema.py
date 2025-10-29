#!/usr/bin/env python3
"""
Script para corrigir o schema do banco de dados PostgreSQL no Render
"""

import os
import sys
from app import app, db

def fix_database_schema():
    """Corrige o schema do banco de dados"""
    print("🔧 Corrigindo schema do banco de dados...")
    
    with app.app_context():
        try:
            # Dropar todas as tabelas existentes
            print("🗑️ Removendo tabelas existentes...")
            db.drop_all()
            
            # Criar todas as tabelas com o schema correto
            print("🏗️ Criando tabelas com schema correto...")
            db.create_all()
            
            print("✅ Schema do banco de dados corrigido com sucesso!")
            
            # Criar usuário admin
            from app import User
            admin_user = User.query.filter_by(email='arthurnavarro160203@gmail.com').first()
            
            if not admin_user:
                print("👤 Criando usuário administrador...")
                admin_user = User(
                    username='admin',
                    email='arthurnavarro160203@gmail.com',
                    empresa='Sistema',
                    role='admin'
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Usuário administrador criado!")
                print("📧 Email: arthurnavarro160203@gmail.com")
                print("🔑 Senha: admin123")
            else:
                print("✅ Usuário administrador já existe!")
            
            print("🎉 Banco de dados corrigido com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao corrigir banco de dados: {e}")
            sys.exit(1)

if __name__ == '__main__':
    fix_database_schema()
