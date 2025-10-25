#!/usr/bin/env python3
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
