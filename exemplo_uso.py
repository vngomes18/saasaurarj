#!/usr/bin/env python3
"""
Script de exemplo para demonstrar como usar o SaaS Sistema de Gestão
Este script cria dados de exemplo para testar o sistema
"""

from app import app, db, User, Produto, Cliente, Venda, ItemVenda
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def criar_dados_exemplo():
    """Cria dados de exemplo para demonstrar o sistema"""
    
    with app.app_context():
        # Criar tabelas
        db.create_all()
        
        print("Criando dados de exemplo...")
        
        # 1. Criar usuário de exemplo
        print("Criando usuario...")
        usuario = User(
            username="admin",
            email="admin@sistema.com",
            password_hash=generate_password_hash("123456"),
            empresa="Empresa Exemplo LTDA"
        )
        db.session.add(usuario)
        db.session.commit()
        print(f"Usuario criado: {usuario.username}")
        
        # 2. Criar produtos de exemplo
        print("Criando produtos...")
        produtos_exemplo = [
            {
                "nome": "Smartphone Samsung Galaxy",
                "descricao": "Smartphone Android com 128GB de armazenamento",
                "preco": 899.99,
                "estoque_atual": 25,
                "estoque_minimo": 5,
                "categoria": "Eletrônicos",
                "codigo_barras": "7891234567890"
            },
            {
                "nome": "Notebook Dell Inspiron",
                "descricao": "Notebook com processador Intel i5, 8GB RAM",
                "preco": 2499.99,
                "estoque_atual": 8,
                "estoque_minimo": 3,
                "categoria": "Eletrônicos",
                "codigo_barras": "7891234567891"
            },
            {
                "nome": "Camiseta Polo",
                "descricao": "Camiseta polo masculina 100% algodão",
                "preco": 79.99,
                "estoque_atual": 50,
                "estoque_minimo": 10,
                "categoria": "Roupas",
                "codigo_barras": "7891234567892"
            },
            {
                "nome": "Café em Grãos Premium",
                "descricao": "Café especial torrado, pacote 500g",
                "preco": 24.99,
                "estoque_atual": 2,  # Estoque baixo para demonstrar alertas
                "estoque_minimo": 5,
                "categoria": "Alimentícios",
                "codigo_barras": "7891234567893"
            },
            {
                "nome": "Livro Python para Iniciantes",
                "descricao": "Guia completo de programação Python",
                "preco": 49.99,
                "estoque_atual": 15,
                "estoque_minimo": 5,
                "categoria": "Livros",
                "codigo_barras": "7891234567894"
            }
        ]
        
        produtos_criados = []
        for produto_data in produtos_exemplo:
            produto = Produto(
                nome=produto_data["nome"],
                descricao=produto_data["descricao"],
                preco=produto_data["preco"],
                estoque_atual=produto_data["estoque_atual"],
                estoque_minimo=produto_data["estoque_minimo"],
                categoria=produto_data["categoria"],
                codigo_barras=produto_data["codigo_barras"],
                user_id=usuario.id
            )
            db.session.add(produto)
            produtos_criados.append(produto)
        
        db.session.commit()
        print(f"{len(produtos_criados)} produtos criados")
        
        # 3. Criar clientes de exemplo
        print("Criando clientes...")
        clientes_exemplo = [
            {
                "nome": "João Silva",
                "email": "joao.silva@email.com",
                "telefone": "(11) 99999-1111",
                "endereco": "Rua das Flores, 123, Centro, São Paulo - SP",
                "cpf_cnpj": "123.456.789-00"
            },
            {
                "nome": "Maria Santos",
                "email": "maria.santos@email.com",
                "telefone": "(11) 99999-2222",
                "endereco": "Av. Paulista, 456, Bela Vista, São Paulo - SP",
                "cpf_cnpj": "987.654.321-00"
            },
            {
                "nome": "Pedro Oliveira",
                "email": "pedro.oliveira@email.com",
                "telefone": "(11) 99999-3333",
                "endereco": "Rua Augusta, 789, Consolação, São Paulo - SP",
                "cpf_cnpj": "456.789.123-00"
            }
        ]
        
        clientes_criados = []
        for cliente_data in clientes_exemplo:
            cliente = Cliente(
                nome=cliente_data["nome"],
                email=cliente_data["email"],
                telefone=cliente_data["telefone"],
                endereco=cliente_data["endereco"],
                cpf_cnpj=cliente_data["cpf_cnpj"],
                user_id=usuario.id
            )
            db.session.add(cliente)
            clientes_criados.append(cliente)
        
        db.session.commit()
        print(f"{len(clientes_criados)} clientes criados")
        
        # 4. Criar vendas de exemplo
        print("Criando vendas...")
        vendas_exemplo = [
            {
                "cliente_id": clientes_criados[0].id,
                "valor_total": 899.99,
                "forma_pagamento": "cartao_credito",
                "observacoes": "Venda realizada via telefone",
                "itens": [
                    {"produto_id": produtos_criados[0].id, "quantidade": 1, "preco_unitario": 899.99}
                ]
            },
            {
                "cliente_id": clientes_criados[1].id,
                "valor_total": 2579.98,
                "forma_pagamento": "pix",
                "observacoes": "Cliente VIP - desconto aplicado",
                "itens": [
                    {"produto_id": produtos_criados[1].id, "quantidade": 1, "preco_unitario": 2499.99},
                    {"produto_id": produtos_criados[2].id, "quantidade": 1, "preco_unitario": 79.99}
                ]
            },
            {
                "cliente_id": None,  # Cliente avulso
                "valor_total": 74.98,
                "forma_pagamento": "dinheiro",
                "observacoes": "Venda no balcão",
                "itens": [
                    {"produto_id": produtos_criados[2].id, "quantidade": 2, "preco_unitario": 79.99},
                    {"produto_id": produtos_criados[3].id, "quantidade": 1, "preco_unitario": 24.99}
                ]
            }
        ]
        
        for i, venda_data in enumerate(vendas_exemplo):
            # Criar venda
            venda = Venda(
                cliente_id=venda_data["cliente_id"],
                valor_total=venda_data["valor_total"],
                forma_pagamento=venda_data["forma_pagamento"],
                observacoes=venda_data["observacoes"],
                user_id=usuario.id,
                data_venda=datetime.now() - timedelta(days=i+1)  # Vendas em dias diferentes
            )
            db.session.add(venda)
            db.session.flush()  # Para obter o ID da venda
            
            # Criar itens da venda
            for item_data in venda_data["itens"]:
                item = ItemVenda(
                    venda_id=venda.id,
                    produto_id=item_data["produto_id"],
                    quantidade=item_data["quantidade"],
                    preco_unitario=item_data["preco_unitario"],
                    subtotal=item_data["quantidade"] * item_data["preco_unitario"]
                )
                db.session.add(item)
                
                # Atualizar estoque
                produto = Produto.query.get(item_data["produto_id"])
                produto.estoque_atual -= item_data["quantidade"]
        
        db.session.commit()
        print(f"{len(vendas_exemplo)} vendas criadas")
        
        print("\n" + "=" * 60)
        print("DADOS DE EXEMPLO CRIADOS COM SUCESSO!")
        print("=" * 60)
        print("\nResumo dos dados criados:")
        print(f"Usuario: admin@sistema.com (senha: 123456)")
        print(f"Produtos: {len(produtos_criados)}")
        print(f"Clientes: {len(clientes_criados)}")
        print(f"Vendas: {len(vendas_exemplo)}")
        print("\nPara testar o sistema:")
        print("1. Execute: python run.py")
        print("2. Acesse: http://localhost:5000")
        print("3. Faca login com: admin@sistema.com / 123456")
        print("\nFuncionalidades para testar:")
        print("- Dashboard com metricas e graficos")
        print("- Lista de produtos (alguns com estoque baixo)")
        print("- Base de clientes cadastrados")
        print("- Historico de vendas")
        print("- Sistema de busca e filtros")
        print("=" * 60)

if __name__ == "__main__":
    try:
        criar_dados_exemplo()
    except Exception as e:
        print(f"Erro ao criar dados de exemplo: {e}")
        print("Certifique-se de que o banco de dados esta configurado corretamente")

