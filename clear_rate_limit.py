#!/usr/bin/env python3
"""
Script para limpar rate limiting em desenvolvimento
"""

import os
import sys
import time
from app import app

def clear_rate_limits():
    """Limpa todos os rate limits"""
    print("🧹 Limpando rate limits...")
    
    # Limpar rate limiting do Flask-Limiter
    if hasattr(app, 'limiter') and app.limiter:
        try:
            # Limpar storage do limiter
            app.limiter.storage.clear()
            print("✅ Flask-Limiter storage limpo")
        except Exception as e:
            print(f"⚠️ Erro ao limpar Flask-Limiter: {e}")
    
    # Limpar middleware de segurança
    try:
        from security_middleware import SecurityMiddleware
        # Reinicializar middleware
        if hasattr(app, 'security_middleware'):
            app.security_middleware.failed_attempts.clear()
            app.security_middleware.blocked_ips.clear()
            print("✅ Middleware de segurança limpo")
    except Exception as e:
        print(f"⚠️ Erro ao limpar middleware: {e}")
    
    print("🎉 Rate limits limpos com sucesso!")
    print("💡 Dica: Reinicie o servidor para aplicar as mudanças")

if __name__ == '__main__':
    with app.app_context():
        clear_rate_limits()
