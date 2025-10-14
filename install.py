#!/usr/bin/env python3
"""
Script de instalação e configuração inicial do SaaS Sistema de Gestão
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Imprime o cabeçalho do instalador"""
    print("=" * 60)
    print("🚀 SaaS SISTEMA DE GESTÃO - INSTALADOR")
    print("=" * 60)
    print("Sistema completo para controle de estoque e vendas")
    print("Desenvolvido com Python Flask, HTML, CSS e JavaScript")
    print("=" * 60)

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print("\n📋 Verificando versão do Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 ou superior é necessário!")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def create_virtual_environment():
    """Cria ambiente virtual se não existir"""
    print("\n🔧 Configurando ambiente virtual...")
    
    venv_path = "venv"
    if os.path.exists(venv_path):
        print("✅ Ambiente virtual já existe")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        print("✅ Ambiente virtual criado com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao criar ambiente virtual")
        return False

def get_activation_command():
    """Retorna comando para ativar ambiente virtual baseado no OS"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def install_dependencies():
    """Instala dependências do projeto"""
    print("\n📦 Instalando dependências...")
    
    # Determina o comando pip baseado no OS
    if platform.system() == "Windows":
        pip_command = os.path.join("venv", "Scripts", "pip")
    else:
        pip_command = os.path.join("venv", "bin", "pip")
    
    try:
        subprocess.run([pip_command, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def create_directories():
    """Cria diretórios necessários"""
    print("\n📁 Criando diretórios...")
    
    directories = [
        "instance",
        "static/uploads",
        "static/images",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Diretórios criados")

def create_env_file():
    """Cria arquivo .env se não existir"""
    print("\n⚙️ Configurando variáveis de ambiente...")
    
    if os.path.exists(".env"):
        print("✅ Arquivo .env já existe")
        return
    
    env_content = """# Configurações do Sistema SaaS
SECRET_KEY=sua-chave-secreta-super-segura-aqui
SQLALCHEMY_DATABASE_URI=sqlite:///saas_sistema.db
FLASK_ENV=development
FLASK_DEBUG=True

# Configurações de Email (opcional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=sua-senha-de-app

# Configurações de Upload (opcional)
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("✅ Arquivo .env criado")

def print_instructions():
    """Imprime instruções de uso"""
    activation_cmd = get_activation_command()
    
    print("\n" + "=" * 60)
    print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("\n📋 Próximos passos:")
    print(f"1. Ative o ambiente virtual: {activation_cmd}")
    print("2. Execute o sistema: python run.py")
    print("3. Acesse: http://localhost:5000")
    print("\n🔐 Para primeiro acesso:")
    print("- Vá para: http://localhost:5000/register")
    print("- Crie sua conta de usuário")
    print("- Faça login e comece a usar!")
    print("\n📚 Documentação completa no README.md")
    print("=" * 60)

def main():
    """Função principal do instalador"""
    print_header()
    
    # Verificações e instalação
    if not check_python_version():
        return False
    
    if not create_virtual_environment():
        return False
    
    if not install_dependencies():
        return False
    
    create_directories()
    create_env_file()
    
    print_instructions()
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Instalação falhou!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Instalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)

