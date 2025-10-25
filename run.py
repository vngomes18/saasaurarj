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
        try:
            # Verificar se é PostgreSQL e se há problemas de schema
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            # Se não há tabelas ou se há problemas de schema, recriar tudo
            if not existing_tables or 'user' not in existing_tables:
                print("Recriando schema do banco de dados...")
                db.drop_all()
                db.create_all()
                print("Schema recriado com sucesso!")
            else:
                # Verificar se a tabela user tem as colunas necessárias
                try:
                    from app import User
                    User.query.first()  # Teste simples
                    print("Schema do banco de dados OK!")
                except Exception as schema_error:
                    print(f"Problema de schema detectado: {schema_error}")
                    print("Recriando schema do banco de dados...")
                    db.drop_all()
                    db.create_all()
                    print("Schema recriado com sucesso!")
            
            # Verificar se já existe um usuário admin
            from app import User
            admin_user = User.query.filter_by(email='arthurnavarro160203@gmail.com').first()
            
            if not admin_user:
                print("Criando usuario administrador...")
                admin_user = User(
                    username='admin',
                    email='arthurnavarro160203@gmail.com',
                    empresa='Sistema',
                    role='admin'
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print("Usuario administrador criado!")
                print("Email: arthurnavarro160203@gmail.com")
                print("Senha: admin123")
            else:
                print("Usuario administrador ja existe!")
                
        except Exception as e:
            print(f"Erro ao inicializar banco de dados: {e}")
            print("Tentando recriar schema...")
            try:
                db.drop_all()
                db.create_all()
                print("Schema recriado com sucesso!")
            except Exception as recreate_error:
                print(f"Erro ao recriar schema: {recreate_error}")
                # Continuar mesmo com erro para não quebrar o deploy
    
    # Executar aplicação
    print(">> Iniciando SaaS Sistema de Gestao...")
    print(">> Dashboard: http://localhost:5000")
    print(">> Login: http://localhost:5000/login")
    print(">> Registro: http://localhost:5000/register")
    
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    )
