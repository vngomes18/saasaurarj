#!/usr/bin/env python3
"""
Script para criar índices no banco de dados
Otimiza consultas frequentes adicionando índices nas colunas mais consultadas
"""

import sqlite3
import os
from datetime import datetime

def create_indexes():
    """Cria índices para otimizar consultas no banco de dados"""
    
    # Caminho do banco de dados
    db_path = 'instance/saas_sistema.db'
    
    if not os.path.exists(db_path):
        print("ERRO: Banco de dados nao encontrado!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Criando indices para otimizacao do banco de dados...")
        
        # Lista de índices para criar
        indexes = [
            # Índices para tabela User
            ("idx_user_username", "CREATE INDEX IF NOT EXISTS idx_user_username ON user(username)"),
            ("idx_user_email", "CREATE INDEX IF NOT EXISTS idx_user_email ON user(email)"),
            ("idx_user_empresa", "CREATE INDEX IF NOT EXISTS idx_user_empresa ON user(empresa)"),
            ("idx_user_role", "CREATE INDEX IF NOT EXISTS idx_user_role ON user(role)"),
            ("idx_user_google_id", "CREATE INDEX IF NOT EXISTS idx_user_google_id ON user(google_id)"),
            ("idx_user_created_at", "CREATE INDEX IF NOT EXISTS idx_user_created_at ON user(created_at)"),
            
            # Índices para tabela Produto
            ("idx_produto_nome", "CREATE INDEX IF NOT EXISTS idx_produto_nome ON produto(nome)"),
            ("idx_produto_preco", "CREATE INDEX IF NOT EXISTS idx_produto_preco ON produto(preco)"),
            ("idx_produto_estoque_atual", "CREATE INDEX IF NOT EXISTS idx_produto_estoque_atual ON produto(estoque_atual)"),
            ("idx_produto_categoria", "CREATE INDEX IF NOT EXISTS idx_produto_categoria ON produto(categoria)"),
            ("idx_produto_codigo_barras", "CREATE INDEX IF NOT EXISTS idx_produto_codigo_barras ON produto(codigo_barras)"),
            ("idx_produto_created_at", "CREATE INDEX IF NOT EXISTS idx_produto_created_at ON produto(created_at)"),
            ("idx_produto_user_id", "CREATE INDEX IF NOT EXISTS idx_produto_user_id ON produto(user_id)"),
            
            # Índices para tabela Venda
            ("idx_venda_data_venda", "CREATE INDEX IF NOT EXISTS idx_venda_data_venda ON venda(data_venda)"),
            ("idx_venda_valor_total", "CREATE INDEX IF NOT EXISTS idx_venda_valor_total ON venda(valor_total)"),
            ("idx_venda_status", "CREATE INDEX IF NOT EXISTS idx_venda_status ON venda(status)"),
            ("idx_venda_forma_pagamento", "CREATE INDEX IF NOT EXISTS idx_venda_forma_pagamento ON venda(forma_pagamento)"),
            ("idx_venda_user_id", "CREATE INDEX IF NOT EXISTS idx_venda_user_id ON venda(user_id)"),
            ("idx_venda_cliente_id", "CREATE INDEX IF NOT EXISTS idx_venda_cliente_id ON venda(cliente_id)"),
            
            # Índices para tabela Cliente
            ("idx_cliente_nome", "CREATE INDEX IF NOT EXISTS idx_cliente_nome ON cliente(nome)"),
            ("idx_cliente_email", "CREATE INDEX IF NOT EXISTS idx_cliente_email ON cliente(email)"),
            ("idx_cliente_created_at", "CREATE INDEX IF NOT EXISTS idx_cliente_created_at ON cliente(created_at)"),
            ("idx_cliente_user_id", "CREATE INDEX IF NOT EXISTS idx_cliente_user_id ON cliente(user_id)"),
            
            # Índices para tabela Fornecedor
            ("idx_fornecedor_nome", "CREATE INDEX IF NOT EXISTS idx_fornecedor_nome ON fornecedor(nome)"),
            ("idx_fornecedor_email", "CREATE INDEX IF NOT EXISTS idx_fornecedor_email ON fornecedor(email)"),
            ("idx_fornecedor_created_at", "CREATE INDEX IF NOT EXISTS idx_fornecedor_created_at ON fornecedor(created_at)"),
            ("idx_fornecedor_user_id", "CREATE INDEX IF NOT EXISTS idx_fornecedor_user_id ON fornecedor(user_id)"),
            
            # Índices para tabela Compra
            ("idx_compra_data_compra", "CREATE INDEX IF NOT EXISTS idx_compra_data_compra ON compra(data_compra)"),
            ("idx_compra_valor_total", "CREATE INDEX IF NOT EXISTS idx_compra_valor_total ON compra(valor_total)"),
            ("idx_compra_user_id", "CREATE INDEX IF NOT EXISTS idx_compra_user_id ON compra(user_id)"),
            ("idx_compra_fornecedor_id", "CREATE INDEX IF NOT EXISTS idx_compra_fornecedor_id ON compra(fornecedor_id)"),
            
            # Índices para tabela ItemVenda
            ("idx_item_venda_venda_id", "CREATE INDEX IF NOT EXISTS idx_item_venda_venda_id ON item_venda(venda_id)"),
            ("idx_item_venda_produto_id", "CREATE INDEX IF NOT EXISTS idx_item_venda_produto_id ON item_venda(produto_id)"),
            
            # Índices para tabela ItemCompra
            ("idx_item_compra_compra_id", "CREATE INDEX IF NOT EXISTS idx_item_compra_compra_id ON item_compra(compra_id)"),
            ("idx_item_compra_produto_id", "CREATE INDEX IF NOT EXISTS idx_item_compra_produto_id ON item_compra(produto_id)"),
            
            # Índices para tabela TicketSuporte
            ("idx_ticket_status", "CREATE INDEX IF NOT EXISTS idx_ticket_status ON ticket_suporte(status)"),
            ("idx_ticket_prioridade", "CREATE INDEX IF NOT EXISTS idx_ticket_prioridade ON ticket_suporte(prioridade)"),
            ("idx_ticket_created_at", "CREATE INDEX IF NOT EXISTS idx_ticket_created_at ON ticket_suporte(created_at)"),
            ("idx_ticket_user_id", "CREATE INDEX IF NOT EXISTS idx_ticket_user_id ON ticket_suporte(user_id)"),
            
            # Índices para tabela NotaFiscal
            ("idx_nota_status", "CREATE INDEX IF NOT EXISTS idx_nota_status ON nota_fiscal(status)"),
            ("idx_nota_data_emissao", "CREATE INDEX IF NOT EXISTS idx_nota_data_emissao ON nota_fiscal(data_emissao)"),
            ("idx_nota_user_id", "CREATE INDEX IF NOT EXISTS idx_nota_user_id ON nota_fiscal(user_id)"),
        ]
        
        # Executar criação dos índices
        created_count = 0
        for index_name, sql in indexes:
            try:
                cursor.execute(sql)
                created_count += 1
                print(f"OK - Indice criado: {index_name}")
            except sqlite3.Error as e:
                print(f"ERRO ao criar indice {index_name}: {e}")
        
        conn.commit()
        print(f"\nProcesso concluido!")
        print(f"Total de indices criados: {created_count}")
        
        # Verificar índices criados
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'")
        existing_indexes = cursor.fetchall()
        print(f"Indices existentes: {len(existing_indexes)}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"ERRO no banco de dados: {e}")
        return False
    finally:
        if conn:
            conn.close()

def verify_indexes():
    """Verifica quais índices foram criados"""
    db_path = 'instance/saas_sistema.db'
    
    if not os.path.exists(db_path):
        print("ERRO: Banco de dados nao encontrado!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\nVerificando indices criados...")
        
        cursor.execute("""
            SELECT name, sql 
            FROM sqlite_master 
            WHERE type='index' AND name LIKE 'idx_%'
            ORDER BY name
        """)
        
        indexes = cursor.fetchall()
        
        if indexes:
            print(f"\nIndices encontrados ({len(indexes)}):")
            for name, sql in indexes:
                print(f"  - {name}")
        else:
            print("\nNenhum indice encontrado!")
            
    except sqlite3.Error as e:
        print(f"ERRO ao verificar indices: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("OTIMIZACAO DE BANCO DE DADOS - CRIAR INDICES")
    print("=" * 60)
    
    success = create_indexes()
    
    if success:
        verify_indexes()
        print("\nOtimizacao concluida com sucesso!")
        print("O banco de dados agora esta otimizado para consultas mais rapidas.")
    else:
        print("\nFalha na otimizacao do banco de dados.")
    
    print("=" * 60)
