#!/usr/bin/env python3
"""
Configurações específicas para desenvolvimento
Desabilita rate limiting e outras restrições
"""

import os
from config import Config

class DevConfig(Config):
    """Configurações otimizadas para desenvolvimento"""
    
    # Desabilitar rate limiting
    RATELIMIT_DEFAULT = "10000 per day, 1000 per hour"
    
    # Configurações de sessão mais permissivas
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    
    # CSRF mais permissivo
    WTF_CSRF_SSL_STRICT = False
    
    # Debug habilitado
    DEBUG = True
    FLASK_ENV = 'development'
    
    # Headers de segurança relaxados
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',  # Mais permissivo
    }

# Usar configuração de desenvolvimento
config = {
    'development': DevConfig,
    'production': Config,
    'testing': Config,
    'default': DevConfig
}
