#!/usr/bin/env python3
"""
Script para migração gradual da API
Remove duplicações e consolida em estrutura unificada
"""

import os
import shutil
from datetime import datetime

def backup_original_files():
    """Cria backup dos arquivos originais"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_api_{timestamp}"
    
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup dos arquivos originais
    files_to_backup = ['api_routes.py', 'app.py']
    
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, f"{backup_dir}/{file}")
            print(f"Backup criado: {backup_dir}/{file}")
    
    return backup_dir

def create_migration_plan():
    """Cria plano de migração"""
    plan = """
# 📋 PLANO DE MIGRAÇÃO DA API

## ✅ Fase 1: Preparação (Concluída)
- [x] Criar API unificada (api_unified.py)
- [x] Implementar autenticação híbrida
- [x] Padronizar respostas JSON
- [x] Backup dos arquivos originais

## 🔄 Fase 2: Migração Gradual
- [ ] Substituir api_routes.py por api_unified.py
- [ ] Remover endpoints duplicados do app.py
- [ ] Manter compatibilidade com frontend React
- [ ] Testar todos os endpoints

## 🧪 Fase 3: Testes
- [ ] Testar autenticação (sessão + JWT)
- [ ] Testar CRUD de produtos
- [ ] Testar CRUD de clientes
- [ ] Testar dashboard
- [ ] Testar integração React

## 🚀 Fase 4: Deploy
- [ ] Deploy em desenvolvimento
- [ ] Monitorar logs
- [ ] Ajustar se necessário
- [ ] Deploy em produção

## 📊 Benefícios da Migração:
1. ✅ Elimina duplicação de endpoints
2. ✅ Autenticação unificada (sessão + JWT)
3. ✅ Estrutura mais limpa e organizada
4. ✅ Melhor manutenibilidade
5. ✅ Compatibilidade total com React frontend
"""
    
    with open('MIGRATION_PLAN.md', 'w', encoding='utf-8') as f:
        f.write(plan)
    
    print("Plano de migracao criado: MIGRATION_PLAN.md")

def create_compatibility_layer():
    """Cria camada de compatibilidade para migração gradual"""
    compatibility_code = '''
# ========== CAMADA DE COMPATIBILIDADE ==========
"""
Camada de compatibilidade para migração gradual
Mantém endpoints antigos funcionando durante a transição
"""

from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import jwt_required, get_jwt_identity

# Blueprint de compatibilidade
compat_api = Blueprint('compat_api', __name__, url_prefix='/api/compat')

@compat_api.route('/produtos')
def compat_produtos():
    """Endpoint de compatibilidade para produtos"""
    # Redirecionar para nova API
    from api_unified import api_produtos
    return api_produtos()

@compat_api.route('/clientes')
def compat_clientes():
    """Endpoint de compatibilidade para clientes"""
    # Redirecionar para nova API
    from api_unified import api_clientes
    return api_clientes()

@compat_api.route('/dashboard')
def compat_dashboard():
    """Endpoint de compatibilidade para dashboard"""
    # Redirecionar para nova API
    from api_unified import api_dashboard
    return api_dashboard()
'''
    
    with open('api_compatibility.py', 'w', encoding='utf-8') as f:
        f.write(compatibility_code)
    
    print("Camada de compatibilidade criada: api_compatibility.py")

def create_test_script():
    """Cria script de teste para validar a migração"""
    test_script = '''#!/usr/bin/env python3
"""
Script de teste para validar migração da API
"""

import requests
import json

def test_api_endpoints():
    """Testa todos os endpoints da API"""
    base_url = "http://localhost:5000/api"
    
    # Endpoints para testar
    endpoints = [
        "/dashboard",
        "/produtos",
        "/clientes", 
        "/vendas",
        "/auth/me",
        "/stats"
    ]
    
    print("🧪 Testando endpoints da API...")
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK")
            else:
                print(f"❌ {endpoint} - Erro {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Erro: {e}")

if __name__ == '__main__':
    test_api_endpoints()
'''
    
    with open('test_api_migration.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("Script de teste criado: test_api_migration.py")

def main():
    """Executa a migração"""
    print("Iniciando migracao da API...")
    
    # 1. Backup dos arquivos originais
    backup_dir = backup_original_files()
    print(f"Backup criado em: {backup_dir}")
    
    # 2. Criar plano de migração
    create_migration_plan()
    
    # 3. Criar camada de compatibilidade
    create_compatibility_layer()
    
    # 4. Criar script de teste
    create_test_script()
    
    print("""
Migracao preparada com sucesso!

Proximos passos:
1. Revisar api_unified.py
2. Executar: python test_api_migration.py
3. Substituir api_routes.py por api_unified.py
4. Remover endpoints duplicados do app.py
5. Testar integracao com React frontend

Arquivos criados:
- api_unified.py (API unificada)
- api_compatibility.py (Camada de compatibilidade)
- test_api_migration.py (Script de teste)
- MIGRATION_PLAN.md (Plano de migracao)
- backup_api_*/ (Backup dos originais)
""")

if __name__ == '__main__':
    main()
