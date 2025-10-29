#!/usr/bin/env python3
"""
Script para limpar o banco de dados e remover usuários existentes
"""

from app import app, db, User, Produto, Cliente, Venda, ItemVenda

def limpar_banco():
    """Remove todos os dados do banco de dados"""
    
    with app.app_context():
        print("Limpando banco de dados...")
        
        # Deletar todas as tabelas em ordem (respeitando foreign keys)
        print("Removendo itens de venda...")
        ItemVenda.query.delete()
        
        print("Removendo vendas...")
        Venda.query.delete()
        
        print("Removendo clientes...")
        Cliente.query.delete()
        
        print("Removendo produtos...")
        Produto.query.delete()
        
        print("Removendo usuarios...")
        User.query.delete()
        
        # Commit das mudanças
        db.session.commit()
        
        print("Banco de dados limpo com sucesso!")
        print("\nAgora você pode:")
        print("1. Criar uma nova conta em http://localhost:5000/register")
        print("2. Ou executar 'python exemplo_uso.py' para criar dados de exemplo")

if __name__ == "__main__":
    try:
        limpar_banco()
    except Exception as e:
        print(f"Erro ao limpar banco: {e}")
