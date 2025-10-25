#!/usr/bin/env python3
"""
Script para testar a API
"""

import requests
import json

def test_api():
    base_url = "http://localhost:5000"
    
    print("Testando API...")
    
    # Teste 1: Login
    print("\n1. Testando login...")
    login_data = {
        "email": "admin@sistema.com",
        "password": "123456"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                print("Login bem-sucedido!")
                token = data['access_token']
                
                # Teste 2: Buscar produtos
                print("\n2. Testando busca de produtos...")
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                response = requests.get(
                    f"{base_url}/api/produtos",
                    headers=headers
                )
                
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text}")
                
                if response.status_code == 200:
                    print("Busca de produtos bem-sucedida!")
                else:
                    print("Erro na busca de produtos")
            else:
                print("Token não encontrado na resposta")
        else:
            print("Erro no login")
            
    except Exception as e:
        print(f"Erro na requisição: {e}")

if __name__ == "__main__":
    test_api()
