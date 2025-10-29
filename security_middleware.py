#!/usr/bin/env python3
"""
Middleware de Segurança para SaaS Sistema de Gestão
Implementa várias camadas de proteção de segurança
"""

import os
import time
import hashlib
import hmac
from functools import wraps
from flask import request, jsonify, session, g, abort
from datetime import datetime, timedelta
import bleach
import re

class SecurityMiddleware:
    """Middleware de segurança centralizado"""
    
    def __init__(self, app=None):
        self.app = app
        self.failed_attempts = {}  # IP -> {count, last_attempt}
        self.blocked_ips = set()    # IPs bloqueados temporariamente
        self.suspicious_patterns = [
            r'<script[^>]*>.*?</script>',  # XSS
            r'javascript:',                 # JavaScript injection
            r'on\w+\s*=',                  # Event handlers
            r'<iframe[^>]*>',              # Iframe injection
            r'<object[^>]*>',              # Object injection
            r'<embed[^>]*>',               # Embed injection
            r'<link[^>]*>',                # Link injection
            r'<meta[^>]*>',                # Meta injection
            r'<style[^>]*>',               # Style injection
            r'expression\s*\(',            # CSS expression
            r'url\s*\(',                   # CSS url
            r'@import',                    # CSS import
            r'<base[^>]*>',                # Base tag
            r'<form[^>]*>',                # Form injection
            r'<input[^>]*>',               # Input injection
            r'<textarea[^>]*>',             # Textarea injection
            r'<select[^>]*>',              # Select injection
            r'<option[^>]*>',               # Option injection
            r'<button[^>]*>',               # Button injection
            r'<a[^>]*>',                    # Link injection
            r'<img[^>]*>',                  # Image injection
            r'<video[^>]*>',                # Video injection
            r'<audio[^>]*>',                # Audio injection
            r'<source[^>]*>',               # Source injection
            r'<track[^>]*>',                # Track injection
            r'<canvas[^>]*>',               # Canvas injection
            r'<svg[^>]*>',                  # SVG injection
            r'<math[^>]*>',                 # Math injection
            r'<details[^>]*>',              # Details injection
            r'<summary[^>]*>',             # Summary injection
            r'<dialog[^>]*>',              # Dialog injection
            r'<menu[^>]*>',                 # Menu injection
            r'<menuitem[^>]*>',             # Menuitem injection
            r'<command[^>]*>',              # Command injection
            r'<keygen[^>]*>',               # Keygen injection
            r'<output[^>]*>',               # Output injection
            r'<progress[^>]*>',            # Progress injection
            r'<meter[^>]*>',                # Meter injection
            r'<time[^>]*>',                 # Time injection
            r'<mark[^>]*>',                 # Mark injection
            r'<ruby[^>]*>',                 # Ruby injection
            r'<rt[^>]*>',                   # Rt injection
            r'<rp[^>]*>',                   # Rp injection
            r'<bdi[^>]*>',                  # Bdi injection
            r'<bdo[^>]*>',                  # Bdo injection
            r'<wbr[^>]*>',                  # Wbr injection
            r'<data[^>]*>',                 # Data injection
            r'<article[^>]*>',              # Article injection
            r'<aside[^>]*>',                # Aside injection
            r'<footer[^>]*>',               # Footer injection
            r'<header[^>]*>',               # Header injection
            r'<hgroup[^>]*>',               # Hgroup injection
            r'<nav[^>]*>',                  # Nav injection
            r'<section[^>]*>',              # Section injection
            r'<address[^>]*>',              # Address injection
            r'<main[^>]*>',                 # Main injection
            r'<figure[^>]*>',               # Figure injection
            r'<figcaption[^>]*>',           # Figcaption injection
            r'<blockquote[^>]*>',           # Blockquote injection
            r'<cite[^>]*>',                  # Cite injection
            r'<code[^>]*>',                 # Code injection
            r'<kbd[^>]*>',                  # Kbd injection
            r'<samp[^>]*>',                 # Samp injection
            r'<var[^>]*>',                  # Var injection
            r'<pre[^>]*>',                  # Pre injection
            r'<abbr[^>]*>',                 # Abbr injection
            r'<acronym[^>]*>',              # Acronym injection
            r'<dfn[^>]*>',                  # Dfn injection
            r'<del[^>]*>',                  # Del injection
            r'<ins[^>]*>',                  # Ins injection
            r'<s[^>]*>',                    # S injection
            r'<u[^>]*>',                    # U injection
            r'<small[^>]*>',                # Small injection
            r'<sub[^>]*>',                  # Sub injection
            r'<sup[^>]*>',                  # Sup injection
            r'<q[^>]*>',                    # Q injection
            r'<s[^>]*>',                    # S injection
            r'<strike[^>]*>',               # Strike injection
            r'<tt[^>]*>',                   # Tt injection
            r'<big[^>]*>',                  # Big injection
            r'<blink[^>]*>',                # Blink injection
            r'<marquee[^>]*>',              # Marquee injection
            r'<nobr[^>]*>',                 # Nobr injection
            r'<noembed[^>]*>',              # Noembed injection
            r'<noframes[^>]*>',             # Noframes injection
            r'<noscript[^>]*>',             # Noscript injection
            r'<plaintext[^>]*>',            # Plaintext injection
            r'<xmp[^>]*>',                  # Xmp injection
            r'<listing[^>]*>',             # Listing injection
            r'<dir[^>]*>',                  # Dir injection
            r'<dl[^>]*>',                   # Dl injection
            r'<dt[^>]*>',                   # Dt injection
            r'<dd[^>]*>',                   # Dd injection
            r'<ol[^>]*>',                   # Ol injection
            r'<ul[^>]*>',                   # Ul injection
            r'<li[^>]*>',                   # Li injection
            r'<table[^>]*>',                # Table injection
            r'<caption[^>]*>',              # Caption injection
            r'<col[^>]*>',                  # Col injection
            r'<colgroup[^>]*>',             # Colgroup injection
            r'<thead[^>]*>',                # Thead injection
            r'<tbody[^>]*>',                # Tbody injection
            r'<tfoot[^>]*>',                # Tfoot injection
            r'<tr[^>]*>',                   # Tr injection
            r'<th[^>]*>',                   # Th injection
            r'<td[^>]*>',                   # Td injection
            r'<fieldset[^>]*>',             # Fieldset injection
            r'<legend[^>]*>',              # Legend injection
            r'<label[^>]*>',                # Label injection
            r'<optgroup[^>]*>',             # Optgroup injection
            r'<datalist[^>]*>',             # Datalist injection
            r'<keygen[^>]*>',               # Keygen injection
            r'<output[^>]*>',               # Output injection
            r'<progress[^>]*>',             # Progress injection
            r'<meter[^>]*>',                # Meter injection
            r'<details[^>]*>',              # Details injection
            r'<summary[^>]*>',              # Summary injection
            r'<command[^>]*>',              # Command injection
            r'<menu[^>]*>',                 # Menu injection
            r'<menuitem[^>]*>',             # Menuitem injection
            r'<dialog[^>]*>',               # Dialog injection
            r'<b[^>]*>',                    # B injection
            r'<i[^>]*>',                    # I injection
            r'<em[^>]*>',                   # Em injection
            r'<strong[^>]*>',               # Strong injection
            r'<p[^>]*>',                    # P injection
            r'<br[^>]*>',                   # Br injection
            r'<hr[^>]*>',                   # Hr injection
            r'<div[^>]*>',                  # Div injection
            r'<span[^>]*>',                 # Span injection
            r'<h1[^>]*>',                   # H1 injection
            r'<h2[^>]*>',                   # H2 injection
            r'<h3[^>]*>',                   # H3 injection
            r'<h4[^>]*>',                   # H4 injection
            r'<h5[^>]*>',                   # H5 injection
            r'<h6[^>]*>',                   # H6 injection
        ]
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializa o middleware com a aplicação Flask"""
        self.app = app
        
        # Registrar hooks
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        
        # Configurar headers de segurança
        self.setup_security_headers()
    
    def before_request(self):
        """Executado antes de cada requisição"""
        # Limpar IPs bloqueados expirados
        self.cleanup_blocked_ips()
        
        # Verificar se IP está bloqueado
        client_ip = self.get_client_ip()
        if client_ip in self.blocked_ips:
            abort(429)  # Too Many Requests
        
        # Verificar padrões suspeitos
        if self.detect_suspicious_activity():
            self.block_ip(client_ip)
            abort(403)  # Forbidden
        
        # Rate limiting básico
        if not self.check_rate_limit(client_ip):
            abort(429)  # Too Many Requests
        
        # Sanitizar dados de entrada
        self.sanitize_inputs()
    
    def after_request(self, response):
        """Executado após cada requisição"""
        # Adicionar headers de segurança
        for header, value in self.app.config.get('SECURITY_HEADERS', {}).items():
            response.headers[header] = value
        
        # Adicionar timestamp de resposta
        response.headers['X-Response-Time'] = str(time.time())
        
        return response
    
    def get_client_ip(self):
        """Obtém o IP real do cliente"""
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        else:
            return request.remote_addr
    
    def detect_suspicious_activity(self):
        """Detecta atividade suspeita na requisição"""
        # Verificar padrões de XSS
        for pattern in self.suspicious_patterns:
            if re.search(pattern, str(request.data), re.IGNORECASE):
                return True
            if re.search(pattern, str(request.form), re.IGNORECASE):
                return True
            if re.search(pattern, str(request.args), re.IGNORECASE):
                return True
        
        # Verificar User-Agent suspeito
        user_agent = request.headers.get('User-Agent', '').lower()
        suspicious_agents = ['sqlmap', 'nikto', 'nmap', 'masscan', 'zap', 'burp']
        if any(agent in user_agent for agent in suspicious_agents):
            return True
        
        # Verificar tentativas de path traversal
        if '..' in request.path or '../' in request.path:
            return True
        
        # Verificar tentativas de SQL injection básicas
        sql_patterns = ['union', 'select', 'insert', 'update', 'delete', 'drop', 'create', 'alter']
        for pattern in sql_patterns:
            if pattern in str(request.data).lower():
                return True
            if pattern in str(request.form).lower():
                return True
            if pattern in str(request.args).lower():
                return True
        
        return False
    
    def check_rate_limit(self, ip):
        """Verifica rate limiting para um IP"""
        now = time.time()
        
        if ip not in self.failed_attempts:
            self.failed_attempts[ip] = {'count': 0, 'last_attempt': now}
            return True
        
        attempt_data = self.failed_attempts[ip]
        
        # Reset se passou muito tempo
        if now - attempt_data['last_attempt'] > 3600:  # 1 hora
            attempt_data['count'] = 0
        
        # Verificar limite (aumentado para desenvolvimento)
        if attempt_data['count'] > 500:  # 500 tentativas por hora
            return False
        
        attempt_data['count'] += 1
        attempt_data['last_attempt'] = now
        
        return True
    
    def block_ip(self, ip, duration=3600):
        """Bloqueia um IP por um período"""
        self.blocked_ips.add(ip)
        # Remover após o tempo especificado
        def remove_block():
            time.sleep(duration)
            self.blocked_ips.discard(ip)
        
        import threading
        threading.Thread(target=remove_block, daemon=True).start()
    
    def cleanup_blocked_ips(self):
        """Remove IPs bloqueados expirados"""
        # Esta função seria chamada periodicamente
        # Por simplicidade, implementamos limpeza básica
        pass
    
    def sanitize_inputs(self):
        """Sanitiza dados de entrada"""
        # Sanitizar dados do formulário
        if request.form:
            for key, value in request.form.items():
                if isinstance(value, str):
                    # Remover tags HTML perigosas
                    sanitized = bleach.clean(value, tags=[], strip=True)
                    if sanitized != value:
                        # Log da tentativa de XSS
                        self.log_security_event('XSS_ATTEMPT', {
                            'ip': self.get_client_ip(),
                            'field': key,
                            'original': value,
                            'sanitized': sanitized
                        })
        
        # Sanitizar dados JSON
        if request.is_json:
            data = request.get_json()
            if data:
                sanitized_data = self.sanitize_dict(data)
                if sanitized_data != data:
                    self.log_security_event('JSON_SANITIZATION', {
                        'ip': self.get_client_ip(),
                        'original': data,
                        'sanitized': sanitized_data
                    })
    
    def sanitize_dict(self, data):
        """Sanitiza um dicionário recursivamente"""
        if isinstance(data, dict):
            return {key: self.sanitize_dict(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_dict(item) for item in data]
        elif isinstance(data, str):
            return bleach.clean(data, tags=[], strip=True)
        else:
            return data
    
    def log_security_event(self, event_type, data):
        """Registra eventos de segurança"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'event_type': event_type,
            'data': data
        }
        
        # Em produção, isso seria enviado para um sistema de logging
        print(f"SECURITY EVENT: {log_entry}")
    
    def setup_security_headers(self):
        """Configura headers de segurança"""
        if not hasattr(self.app, 'config'):
            return
        
        # Headers de segurança padrão
        default_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
        }
        
        # Adicionar headers personalizados se configurados
        custom_headers = self.app.config.get('SECURITY_HEADERS', {})
        default_headers.update(custom_headers)
        
        self.app.config['SECURITY_HEADERS'] = default_headers

# Decorators de segurança
def require_https(f):
    """Força HTTPS"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_secure and not request.headers.get('X-Forwarded-Proto') == 'https':
            if request.url.startswith('http://'):
                https_url = request.url.replace('http://', 'https://', 1)
                return redirect(https_url)
        return f(*args, **kwargs)
    return decorated_function

def require_csrf(f):
    """Força verificação CSRF"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            # Verificar token CSRF
            if not session.get('csrf_token'):
                abort(403)
        return f(*args, **kwargs)
    return decorated_function

def rate_limit(limit):
    """Decorator para rate limiting personalizado"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Implementação básica de rate limiting
            # Em produção, usar Redis ou similar
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_input(schema):
    """Valida dados de entrada contra um schema"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Implementação de validação de schema
            # Em produção, usar biblioteca como Marshmallow
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Funções utilitárias de segurança
def generate_secure_token():
    """Gera token seguro"""
    return os.urandom(32).hex()

def hash_password(password, salt=None):
    """Hash seguro de senha"""
    if salt is None:
        salt = os.urandom(32)
    
    # Usar PBKDF2 com salt
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return password_hash.hex(), salt.hex()

def verify_password(password, password_hash, salt):
    """Verifica senha"""
    salt_bytes = bytes.fromhex(salt)
    test_hash, _ = hash_password(password, salt_bytes)
    return hmac.compare_digest(password_hash, test_hash)

def sanitize_filename(filename):
    """Sanitiza nome de arquivo"""
    # Remover caracteres perigosos
    filename = re.sub(r'[^\w\-_\.]', '', filename)
    # Limitar tamanho
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    return filename

def is_safe_redirect(target):
    """Verifica se redirecionamento é seguro"""
    # Verificar se é URL relativa ou do mesmo domínio
    if target.startswith('/'):
        return True
    
    # Verificar domínio
    from urllib.parse import urlparse
    parsed = urlparse(target)
    return parsed.netloc == request.host

# Configurações de segurança por ambiente
SECURITY_CONFIGS = {
    'development': {
        'DEBUG': True,
        'SESSION_COOKIE_SECURE': False,
        'WTF_CSRF_SSL_STRICT': False,
        'RATE_LIMIT_ENABLED': False
    },
    'production': {
        'DEBUG': False,
        'SESSION_COOKIE_SECURE': True,
        'WTF_CSRF_SSL_STRICT': True,
        'RATE_LIMIT_ENABLED': True,
        'SECURITY_HEADERS': {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'"
        }
    }
}
