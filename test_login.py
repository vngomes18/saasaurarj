#!/usr/bin/env python3
"""
Script para testar login e registro
"""

import requests
from bs4 import BeautifulSoup

def test_login_page():
    base_url = "http://localhost:5000"
    
    print("Testando página de login...")
    
    try:
        # Testar GET da página de login
        response = requests.get(f"{base_url}/login")
        print(f"GET /login Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Página de login carregada com sucesso!")
            
            # Verificar se há formulário
            soup = BeautifulSoup(response.text, 'html.parser')
            form = soup.find('form')
            if form:
                print("Formulário de login encontrado!")
                
                # Testar POST de login
                print("\nTestando POST de login...")
                login_data = {
                    'email': 'admin@sistema.com',
                    'password': '123456'
                }
                
                # Fazer POST para login
                post_response = requests.post(f"{base_url}/login", data=login_data)
                print(f"POST /login Status: {post_response.status_code}")
                
                if post_response.status_code == 302:  # Redirect após login bem-sucedido
                    print("Login bem-sucedido! (Redirect)")
                elif post_response.status_code == 200:
                    print("Login retornou 200 (pode ter erro)")
                else:
                    print(f"Erro no login: {post_response.status_code}")
                    
            else:
                print("Formulário de login não encontrado!")
        else:
            print(f"Erro ao carregar página de login: {response.status_code}")
            
    except Exception as e:
        print(f"Erro na requisição: {e}")

def test_register_page():
    base_url = "http://localhost:5000"
    
    print("\nTestando página de registro...")
    
    try:
        # Testar GET da página de registro
        response = requests.get(f"{base_url}/register")
        print(f"GET /register Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Página de registro carregada com sucesso!")
            
            # Verificar se há formulário
            soup = BeautifulSoup(response.text, 'html.parser')
            form = soup.find('form')
            if form:
                print("Formulário de registro encontrado!")
            else:
                print("Formulário de registro não encontrado!")
        else:
            print(f"Erro ao carregar página de registro: {response.status_code}")
            
    except Exception as e:
        print(f"Erro na requisição: {e}")

if __name__ == "__main__":
    test_login_page()
    test_register_page()
