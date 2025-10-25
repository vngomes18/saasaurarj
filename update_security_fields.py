#!/usr/bin/env python3
"""
Script para adicionar campos de segurança ao banco de dados
Inclui campos para 2FA, controle de tentativas de login e sessões
"""

import sqlite3
import os
import json
from datetime import datetime

def update_database_security():
    """Adiciona campos de segurança ao banco de dados"""
    
    # Caminho do banco de dados
    db_path = 'instance/saas_sistema.db'
    
    if not os.path.exists(db_path):
        print("ERRO: Banco de dados nao encontrado!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Adicionando campos de seguranca ao banco de dados...")
        
        # Campos para adicionar à tabela user
        security_fields = [
            ("two_factor_enabled", "BOOLEAN DEFAULT 0"),
            ("two_factor_secret", "VARCHAR(32)"),
            ("backup_codes", "TEXT"),
            ("last_login", "DATETIME"),
            ("failed_login_attempts", "INTEGER DEFAULT 0"),
            ("locked_until", "DATETIME")
        ]
        
        # Verificar quais campos já existem
        cursor.execute("PRAGMA table_info(user)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        
        added_count = 0
        for field_name, field_type in security_fields:
            if field_name not in existing_columns:
                try:
                    sql = f"ALTER TABLE user ADD COLUMN {field_name} {field_type}"
                    cursor.execute(sql)
                    added_count += 1
                    print(f"OK - Campo adicionado: {field_name}")
                except sqlite3.Error as e:
                    print(f"ERRO ao adicionar campo {field_name}: {e}")
            else:
                print(f"INFO - Campo ja existe: {field_name}")
        
        conn.commit()
        print(f"\nProcesso concluido!")
        print(f"Total de campos adicionados: {added_count}")
        
        # Verificar estrutura da tabela
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        print(f"\nEstrutura atual da tabela user ({len(columns)} campos):")
        for column in columns:
            print(f"  - {column[1]} ({column[2]})")
        
        return True
        
    except sqlite3.Error as e:
        print(f"ERRO no banco de dados: {e}")
        return False
    finally:
        if conn:
            conn.close()

def create_security_indexes():
    """Cria índices para os novos campos de segurança"""
    
    db_path = 'instance/saas_sistema.db'
    
    if not os.path.exists(db_path):
        print("ERRO: Banco de dados nao encontrado!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\nCriando indices para campos de seguranca...")
        
        # Índices para campos de segurança
        security_indexes = [
            ("idx_user_two_factor_enabled", "CREATE INDEX IF NOT EXISTS idx_user_two_factor_enabled ON user(two_factor_enabled)"),
            ("idx_user_last_login", "CREATE INDEX IF NOT EXISTS idx_user_last_login ON user(last_login)"),
            ("idx_user_failed_login_attempts", "CREATE INDEX IF NOT EXISTS idx_user_failed_login_attempts ON user(failed_login_attempts)"),
            ("idx_user_locked_until", "CREATE INDEX IF NOT EXISTS idx_user_locked_until ON user(locked_until)")
        ]
        
        created_count = 0
        for index_name, sql in security_indexes:
            try:
                cursor.execute(sql)
                created_count += 1
                print(f"OK - Indice criado: {index_name}")
            except sqlite3.Error as e:
                print(f"ERRO ao criar indice {index_name}: {e}")
        
        conn.commit()
        print(f"\nTotal de indices de seguranca criados: {created_count}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"ERRO ao criar indices: {e}")
        return False
    finally:
        if conn:
            conn.close()

def verify_security_setup():
    """Verifica se a configuração de segurança está correta"""
    
    db_path = 'instance/saas_sistema.db'
    
    if not os.path.exists(db_path):
        print("ERRO: Banco de dados nao encontrado!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\nVerificando configuração de seguranca...")
        
        # Verificar campos de segurança
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        required_fields = [
            'two_factor_enabled',
            'two_factor_secret', 
            'backup_codes',
            'last_login',
            'failed_login_attempts',
            'locked_until'
        ]
        
        missing_fields = [field for field in required_fields if field not in column_names]
        
        if missing_fields:
            print(f"ATENCAO: Campos faltando: {', '.join(missing_fields)}")
        else:
            print("OK - Todos os campos de seguranca estao presentes")
        
        # Verificar índices de segurança
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_user_%'")
        indexes = cursor.fetchall()
        index_names = [index[0] for index in indexes]
        
        security_indexes = [
            'idx_user_two_factor_enabled',
            'idx_user_last_login',
            'idx_user_failed_login_attempts',
            'idx_user_locked_until'
        ]
        
        missing_indexes = [idx for idx in security_indexes if idx not in index_names]
        
        if missing_indexes:
            print(f"ATENCAO: Indices faltando: {', '.join(missing_indexes)}")
        else:
            print("OK - Todos os indices de seguranca estao presentes")
        
        # Estatísticas de usuários
        cursor.execute("SELECT COUNT(*) FROM user")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM user WHERE two_factor_enabled = 1")
        users_with_2fa = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM user WHERE failed_login_attempts > 0")
        users_with_failed_logins = cursor.fetchone()[0]
        
        print(f"\nEstatisticas de seguranca:")
        print(f"  - Total de usuarios: {total_users}")
        print(f"  - Usuarios com 2FA: {users_with_2fa}")
        print(f"  - Usuarios com tentativas falhadas: {users_with_failed_logins}")
        
    except sqlite3.Error as e:
        print(f"ERRO ao verificar seguranca: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("ATUALIZACAO DE SEGURANCA - SISTEMA SAAS")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success1 = update_database_security()
    success2 = create_security_indexes()
    
    if success1 and success2:
        verify_security_setup()
        print("\nAtualizacao de seguranca concluida com sucesso!")
        print("O sistema agora possui:")
        print("  - Autenticacao de dois fatores (2FA)")
        print("  - Controle de tentativas de login")
        print("  - Bloqueio temporario de contas")
        print("  - Campos de seguranca otimizados")
    else:
        print("\nFalha na atualizacao de seguranca.")
    
    print("=" * 60)
