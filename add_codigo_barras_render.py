#!/usr/bin/env python
"""
Script para adicionar coluna codigo_barras ao ProdutoAuxiliar
Pode ser executado no Render após o deploy
"""
from app import app, db
from sqlalchemy import text

def add_codigo_barras_column():
    with app.app_context():
        try:
            # Verificar se a coluna já existe
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='produto_auxiliar' AND column_name='codigo_barras'
            """))
            
            if result.fetchone():
                print("✅ Coluna codigo_barras já existe!")
                return
            
            # Adicionar a coluna
            print("🔧 Adicionando coluna codigo_barras...")
            db.session.execute(text("""
                ALTER TABLE produto_auxiliar 
                ADD COLUMN codigo_barras VARCHAR(50)
            """))
            db.session.commit()
            print("✅ Coluna codigo_barras adicionada com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_codigo_barras_column()

