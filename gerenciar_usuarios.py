#!/usr/bin/env python3
"""
Script para gerenciar usuários do sistema
"""

from app import app, db, User
import sys
from werkzeug.security import generate_password_hash

def criar_usuario_admin():
    """Cria usuário administrador padrão"""
    
    with app.app_context():
        # Verificar se já existe
        if User.query.filter_by(username='admin').first():
            print("Usuario admin ja existe!")
            return
        
        # Criar usuário admin
        admin = User(
            username='admin',
            email='admin@sistema.com',
            password_hash=generate_password_hash('123456'),
            empresa='Sistema Administrativo',
            role='admin'
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("Usuario admin criado com sucesso!")
        print("Login: admin@sistema.com")
        print("Senha: 123456")

def promover_usuario_admin(identifier, tipo='email'):
    """Promove um usuário para admin pelo email ou username"""
    with app.app_context():
        if tipo == 'email':
            usuario = User.query.filter_by(email=identifier).first()
        else:
            usuario = User.query.filter_by(username=identifier).first()
        
        if not usuario:
            print(f"Usuario com {tipo} '{identifier}' nao encontrado!")
            return
        
        usuario.role = 'admin'
        db.session.commit()
        print(f"Usuario '{identifier}' promovido para admin com sucesso!")

def listar_usuarios():
    """Lista todos os usuários"""
    
    with app.app_context():
        usuarios = User.query.all()
        
        if not usuarios:
            print("Nenhum usuario encontrado!")
            return
        
        print(f"\nTotal de usuarios: {len(usuarios)}")
        print("-" * 60)
        
        for usuario in usuarios:
            print(f"ID: {usuario.id}")
            print(f"Username: {usuario.username}")
            print(f"Email: {usuario.email}")
            print(f"Empresa: {usuario.empresa}")
            print(f"Criado em: {usuario.created_at}")
            print("-" * 60)

def remover_usuario(username):
    """Remove um usuário específico"""
    
    with app.app_context():
        usuario = User.query.filter_by(username=username).first()
        
        if not usuario:
            print(f"Usuario '{username}' nao encontrado!")
            return
        
        # Remover produtos, clientes e vendas do usuário
        from app import Produto, Cliente, Venda, ItemVenda
        
        # Remover itens de venda
        vendas = Venda.query.filter_by(user_id=usuario.id).all()
        for venda in vendas:
            ItemVenda.query.filter_by(venda_id=venda.id).delete()
        
        # Remover vendas
        Venda.query.filter_by(user_id=usuario.id).delete()
        
        # Remover clientes
        Cliente.query.filter_by(user_id=usuario.id).delete()
        
        # Remover produtos
        Produto.query.filter_by(user_id=usuario.id).delete()
        
        # Remover usuário
        db.session.delete(usuario)
        db.session.commit()
        
        print(f"Usuario '{username}' removido com sucesso!")


if __name__ == '__main__':
    # Uso simples via linha de comando
    # Exemplos:
    #  - python gerenciar_usuarios.py criar_admin
    #  - python gerenciar_usuarios.py listar
    #  - python gerenciar_usuarios.py remover <username>
    #  - python gerenciar_usuarios.py promover_admin <email|username> [email|username]
    if len(sys.argv) < 2:
        print("Uso:\n  python gerenciar_usuarios.py criar_admin\n  python gerenciar_usuarios.py listar\n  python gerenciar_usuarios.py remover <username>\n  python gerenciar_usuarios.py promover_admin <identificador> [email|username]")
        sys.exit(0)

    comando = sys.argv[1]
    if comando == 'criar_admin':
        criar_usuario_admin()
    elif comando == 'listar':
        listar_usuarios()
    elif comando == 'remover':
        if len(sys.argv) < 3:
            print("Informe o username: python gerenciar_usuarios.py remover <username>")
        else:
            remover_usuario(sys.argv[2])
    elif comando == 'promover_admin':
        if len(sys.argv) < 3:
            print("Informe o identificador (email ou username): python gerenciar_usuarios.py promover_admin <identificador> [email|username]")
        else:
            identificador = sys.argv[2]
            tipo = sys.argv[3] if len(sys.argv) >= 4 else 'email'
            if tipo not in ('email', 'username'):
                print("Tipo invalido. Use 'email' ou 'username'.")
            else:
                promover_usuario_admin(identificador, tipo)
    else:
        print("Comando desconhecido.")

def menu():
    """Menu interativo"""
    
    while True:
        print("\n" + "=" * 50)
        print("GERENCIADOR DE USUARIOS")
        print("=" * 50)
        print("1. Criar usuario admin")
        print("2. Listar usuarios")
        print("3. Remover usuario")
        print("4. Sair")
        print("=" * 50)
        
        opcao = input("Escolha uma opcao: ").strip()
        
        if opcao == '1':
            criar_usuario_admin()
        elif opcao == '2':
            listar_usuarios()
        elif opcao == '3':
            username = input("Digite o username para remover: ").strip()
            if username:
                confirmar = input(f"Tem certeza que deseja remover '{username}'? (s/n): ").strip().lower()
                if confirmar == 's':
                    remover_usuario(username)
        elif opcao == '4':
            print("Saindo...")
            break
        else:
            print("Opcao invalida!")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\nOperacao cancelada!")
    except Exception as e:
        print(f"Erro: {e}")
