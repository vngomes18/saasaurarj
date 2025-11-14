import os
import secrets
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações base da aplicação com segurança aprimorada"""
    
    # ========== CONFIGURAÇÕES DE SEGURANÇA ==========
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
    
    # Configurações de sessão segura
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'true').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 28800  # 8 horas em segundos
    
    # Configurações CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hora
    WTF_CSRF_SSL_STRICT = os.environ.get('WTF_CSRF_SSL_STRICT', 'false').lower() == 'true'
    
    # Configurações de rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_DEFAULT = "1000 per day, 500 per hour"  # Aumentado para desenvolvimento
    
    # Configurações de segurança de headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self'"
    }
    
    # Configuração inteligente do banco de dados
    def get_database_uri():
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            # Se for PostgreSQL, usar psycopg2
            if database_url.startswith('postgres://'):
                # Converter para o esquema recomendado e garantir o driver psycopg2
                database_url = database_url.replace('postgres://', 'postgresql+psycopg2://', 1)
            elif database_url.startswith('postgresql://') and '+psycopg2://' not in database_url:
                # Tornar o driver explícito quando ausente
                database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
            return database_url
        else:
            # Fallback para SQLite
            return 'sqlite:///saas_sistema.db'
    
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Opções de engine para maior estabilidade com conexões remotas/SSL (Render)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,          # Valida conexões antes de usar para evitar "SSL closed"
        'pool_recycle': 1800,           # Recicla conexões a cada 30 min
        'pool_size': int(os.environ.get('POOL_SIZE', 5)),
        'max_overflow': int(os.environ.get('MAX_OVERFLOW', 10)),
        'connect_args': {
            # Mantém a conexão ativa evitando fechamentos inesperados
            'keepalives': 1,
            'keepalives_idle': 30,
            'keepalives_interval': 10,
            'keepalives_count': 5,
            # Garante SSL quando necessário; também está no URL, mas aqui reforça
            'sslmode': os.environ.get('PGSSLMODE', 'require'),
        }
    }
    
    # Configurações de email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Configurações de upload com segurança
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'static/uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 16777216)  # 16MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx'}
    
    # Configurações de autenticação
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_NUMBERS = True
    PASSWORD_REQUIRE_SPECIAL = True
    
    # Configurações de bloqueio de conta
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = 1800  # 30 minutos em segundos
    
    # Configurações de 2FA
    TOTP_ISSUER_NAME = 'SaaS Sistema'
    BACKUP_CODES_COUNT = 10

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    FLASK_ENV = 'development'
    # Desabilitar rate limiting em desenvolvimento
    RATELIMIT_DEFAULT = "10000 per day, 1000 per hour"

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

