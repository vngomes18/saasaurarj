#!/usr/bin/env python3
"""
Script específico para corrigir o banco de dados no Render
Execute este script no Render para corrigir problemas de schema
"""

import os
import sys
from app import app, db

def fix_render_database():
    """Corrige o banco de dados no Render"""
    print("🔧 Corrigindo banco de dados no Render...")
    
    with app.app_context():
        try:
            # Verificar se estamos no Render
            if os.environ.get('RENDER'):
                print("🌐 Detectado ambiente Render")
            
            # Dropar todas as tabelas
            print("🗑️ Removendo todas as tabelas...")
            db.drop_all()
            
            # Criar todas as tabelas
            print("🏗️ Criando todas as tabelas...")
            db.create_all()
            
            print("✅ Banco de dados corrigido com sucesso!")
            
            # Criar usuário admin
            from app import User
            admin_user = User(
                username='admin',
                email='arthurnavarro160203@gmail.com',
                empresa='Sistema',
                role='admin'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅ Usuário admin criado!")
            print("📧 Email: arthurnavarro160203@gmail.com")
            print("🔑 Senha: admin123")
            
            print("🎉 Correção concluída com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            sys.exit(1)

if __name__ == '__main__':
    fix_render_database()
