#!/usr/bin/env python3
"""
Script para limpar o cache da aplicação
Útil para desenvolvimento e quando dados são atualizados
"""

import os
import shutil
from datetime import datetime

def clear_cache():
    """Limpa o cache da aplicação"""
    
    print("Limpando cache da aplicacao...")
    
    # Diretórios de cache comuns
    cache_dirs = [
        'instance/cache',
        'cache',
        '__pycache__',
        '.cache'
    ]
    
    # Arquivos de cache comuns
    cache_files = [
        'instance/cache.db',
        'cache.db',
        'app.cache'
    ]
    
    cleared_count = 0
    
    # Limpar diretórios de cache
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                print(f"OK - Diretorio removido: {cache_dir}")
                cleared_count += 1
            except Exception as e:
                print(f"ERRO ao remover diretorio {cache_dir}: {e}")
    
    # Limpar arquivos de cache
    for cache_file in cache_files:
        if os.path.exists(cache_file):
            try:
                os.remove(cache_file)
                print(f"OK - Arquivo removido: {cache_file}")
                cleared_count += 1
            except Exception as e:
                print(f"ERRO ao remover arquivo {cache_file}: {e}")
    
    # Limpar arquivos __pycache__ recursivamente
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs[:]:  # Usar slice para modificar a lista durante iteração
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(pycache_path)
                    print(f"OK - __pycache__ removido: {pycache_path}")
                    cleared_count += 1
                except Exception as e:
                    print(f"ERRO ao remover __pycache__ {pycache_path}: {e}")
                dirs.remove(dir_name)  # Não entrar no diretório já removido
    
    print(f"\nProcesso concluido!")
    print(f"Total de itens removidos: {cleared_count}")
    
    if cleared_count == 0:
        print("Nenhum cache encontrado para limpar.")
    else:
        print("Cache limpo com sucesso!")

def show_cache_info():
    """Mostra informações sobre o cache"""
    
    print("\nInformacoes sobre cache:")
    print("-" * 40)
    
    # Verificar Flask-Caching
    try:
        from flask_caching import Cache
        print("Flask-Caching: Disponivel")
    except ImportError:
        print("Flask-Caching: Nao instalado")
    
    # Verificar Redis
    try:
        import redis
        print("Redis: Disponivel")
    except ImportError:
        print("Redis: Nao instalado")
    
    # Verificar diretórios de cache
    cache_dirs = ['instance/cache', 'cache', '__pycache__']
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            print(f"Diretorio {cache_dir}: Existe")
        else:
            print(f"Diretorio {cache_dir}: Nao existe")

if __name__ == "__main__":
    print("=" * 60)
    print("LIMPEZA DE CACHE - SISTEMA SAAS")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    clear_cache()
    show_cache_info()
    
    print("\n" + "=" * 60)
    print("DICA: Execute este script quando:")
    print("- Dados nao estao atualizando corretamente")
    print("- Mudancas no codigo nao estao sendo refletidas")
    print("- Performance esta lenta")
    print("=" * 60)
