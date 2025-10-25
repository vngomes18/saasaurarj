#!/usr/bin/env python3
"""
Script de Auditoria de Segurança para SaaS Sistema de Gestão
Verifica configurações de segurança e gera relatório
"""

import os
import sys
import json
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path

class SecurityAudit:
    """Classe para auditoria de segurança"""
    
    def __init__(self):
        self.audit_results = {
            'timestamp': datetime.now().isoformat(),
            'checks': [],
            'score': 0,
            'recommendations': []
        }
    
    def run_audit(self):
        """Executa auditoria completa"""
        print("Iniciando auditoria de seguranca...")
        
        # Verificações de segurança
        self.check_secret_keys()
        self.check_https_config()
        self.check_session_security()
        self.check_csrf_protection()
        self.check_rate_limiting()
        self.check_input_validation()
        self.check_file_uploads()
        self.check_database_security()
        self.check_dependencies()
        self.check_headers()
        self.check_logging()
        
        # Calcular score
        self.calculate_score()
        
        # Gerar relatório
        self.generate_report()
        
        return self.audit_results
    
    def check_secret_keys(self):
        """Verifica configuração de chaves secretas"""
        check = {
            'name': 'Secret Keys',
            'status': 'PASS',
            'details': [],
            'score': 0
        }
        
        # Verificar SECRET_KEY
        secret_key = os.environ.get('SECRET_KEY')
        if not secret_key:
            check['status'] = 'FAIL'
            check['details'].append('SECRET_KEY não configurada')
            check['score'] = 0
        elif secret_key == 'sua-chave-secreta-super-segura-aqui':
            check['status'] = 'WARN'
            check['details'].append('SECRET_KEY usando valor padrão')
            check['score'] = 2
        elif len(secret_key) < 32:
            check['status'] = 'WARN'
            check['details'].append('SECRET_KEY muito curta (mínimo 32 caracteres)')
            check['score'] = 3
        else:
            check['details'].append('SECRET_KEY configurada corretamente')
            check['score'] = 5
        
        # Verificar JWT_SECRET_KEY
        jwt_key = os.environ.get('JWT_SECRET_KEY')
        if not jwt_key:
            check['status'] = 'FAIL'
            check['details'].append('JWT_SECRET_KEY não configurada')
            check['score'] = 0
        elif len(jwt_key) < 32:
            check['status'] = 'WARN'
            check['details'].append('JWT_SECRET_KEY muito curta')
            check['score'] = 2
        else:
            check['details'].append('JWT_SECRET_KEY configurada corretamente')
            check['score'] = 5
        
        self.audit_results['checks'].append(check)
    
    def check_https_config(self):
        """Verifica configuração HTTPS"""
        check = {
            'name': 'HTTPS Configuration',
            'status': 'PASS',
            'details': [],
            'score': 0
        }
        
        # Verificar se está em produção
        if os.environ.get('FLASK_ENV') == 'production' or os.environ.get('RENDER'):
            # Verificar SESSION_COOKIE_SECURE
            secure_cookies = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
            if secure_cookies:
                check['details'].append('Cookies seguros habilitados')
                check['score'] += 2
            else:
                check['status'] = 'FAIL'
                check['details'].append('SESSION_COOKIE_SECURE não habilitado em produção')
                check['score'] = 0
            
            # Verificar HSTS
            hsts_enabled = os.environ.get('HSTS_ENABLED', 'false').lower() == 'true'
            if hsts_enabled:
                check['details'].append('HSTS habilitado')
                check['score'] += 2
            else:
                check['status'] = 'WARN'
                check['details'].append('HSTS não habilitado')
                check['score'] += 1
        else:
            check['details'].append('Ambiente de desenvolvimento - HTTPS não obrigatório')
            check['score'] = 3
        
        self.audit_results['checks'].append(check)
    
    def check_session_security(self):
        """Verifica segurança de sessão"""
        check = {
            'name': 'Session Security',
            'status': 'PASS',
            'details': [],
            'score': 0
        }
        
        # Verificar SESSION_COOKIE_HTTPONLY
        http_only = os.environ.get('SESSION_COOKIE_HTTPONLY', 'true').lower() == 'true'
        if http_only:
            check['details'].append('HTTPOnly cookies habilitados')
            check['score'] += 2
        else:
            check['status'] = 'FAIL'
            check['details'].append('HTTPOnly cookies não habilitados')
            check['score'] = 0
        
        # Verificar SESSION_COOKIE_SAMESITE
        same_site = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
        if same_site in ['Lax', 'Strict']:
            check['details'].append(f'SameSite cookies configurados como {same_site}')
            check['score'] += 2
        else:
            check['status'] = 'WARN'
            check['details'].append('SameSite cookies não configurados adequadamente')
            check['score'] += 1
        
        # Verificar tempo de sessão
        session_lifetime = int(os.environ.get('PERMANENT_SESSION_LIFETIME', '28800'))
        if session_lifetime <= 28800:  # 8 horas
            check['details'].append(f'Tempo de sessão adequado: {session_lifetime}s')
            check['score'] += 2
        else:
            check['status'] = 'WARN'
            check['details'].append('Tempo de sessão muito longo')
            check['score'] += 1
        
        self.audit_results['checks'].append(check)
    
    def check_csrf_protection(self):
        """Verifica proteção CSRF"""
        check = {
            'name': 'CSRF Protection',
            'status': 'PASS',
            'details': [],
            'score': 0
        }
        
        # Verificar se CSRF está habilitado
        csrf_enabled = os.environ.get('WTF_CSRF_ENABLED', 'true').lower() == 'true'
        if csrf_enabled:
            check['details'].append('CSRF protection habilitado')
            check['score'] += 3
        else:
            check['status'] = 'FAIL'
            check['details'].append('CSRF protection não habilitado')
            check['score'] = 0
        
        # Verificar SSL strict
        ssl_strict = os.environ.get('WTF_CSRF_SSL_STRICT', 'false').lower() == 'true'
        if ssl_strict and os.environ.get('FLASK_ENV') == 'production':
            check['details'].append('CSRF SSL strict habilitado')
            check['score'] += 2
        elif not ssl_strict and os.environ.get('FLASK_ENV') == 'production':
            check['status'] = 'WARN'
            check['details'].append('CSRF SSL strict não habilitado em produção')
            check['score'] += 1
        
        self.audit_results['checks'].append(check)
    
    def check_rate_limiting(self):
        """Verifica rate limiting"""
        check = {
            'name': 'Rate Limiting',
            'status': 'PASS',
            'details': [],
            'score': 0
        }
        
        # Verificar se rate limiting está configurado
        rate_limit_config = os.environ.get('RATELIMIT_DEFAULT')
        if rate_limit_config:
            check['details'].append(f'Rate limiting configurado: {rate_limit_config}')
            check['score'] += 3
        else:
            check['status'] = 'WARN'
            check['details'].append('Rate limiting não configurado')
            check['score'] += 1
        
        # Verificar storage
        storage_url = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
        if storage_url != 'memory://':
            check['details'].append(f'Storage de rate limiting configurado: {storage_url}')
            check['score'] += 2
        else:
            check['status'] = 'WARN'
            check['details'].append('Usando storage em memória para rate limiting')
            check['score'] += 1
        
        self.audit_results['checks'].append(check)
    
    def check_input_validation(self):
        """Verifica validação de entrada"""
        check = {
            'name': 'Input Validation',
            'status': 'PASS',
            'details': [],
            'score': 0
        }
        
        # Verificar se arquivos de validação existem
        if Path('security_validators.py').exists():
            check['details'].append('Validadores de segurança implementados')
            check['score'] += 3
        else:
            check['status'] = 'WARN'
            check['details'].append('Validadores de segurança não encontrados')
            check['score'] += 1
        
        # Verificar middleware de segurança
        if Path('security_middleware.py').exists():
            check['details'].append('Middleware de segurança implementado')
            check['score'] += 3
        else:
            check['status'] = 'WARN'
            check['details'].append('Middleware de segurança não encontrado')
            check['score'] += 1
        
        self.audit_results['checks'].append(check)
    
    def check_file_uploads(self):
        """Verifica segurança de upload de arquivos"""
        check = {
            'name': 'File Upload Security',
            'status': 'PASS',
            'details': [],
            'score': 0
        }
        
        # Verificar tamanho máximo
        max_size = int(os.environ.get('MAX_CONTENT_LENGTH', '16777216'))
        if max_size <= 16777216:  # 16MB
            check['details'].append(f'Tamanho máximo de upload adequado: {max_size} bytes')
            check['score'] += 2
        else:
            check['status'] = 'WARN'
            check['details'].append('Tamanho máximo de upload muito grande')
            check['score'] += 1
        
        # Verificar extensões permitidas
        allowed_exts = os.environ.get('ALLOWED_EXTENSIONS', 'txt,pdf,png,jpg,jpeg,gif,csv,xlsx')
        if allowed_exts:
            check['details'].append(f'Extensões permitidas configuradas: {allowed_exts}')
            check['score'] += 2
        else:
            check['status'] = 'WARN'
            check['details'].append('Extensões permitidas não configuradas')
            check['score'] += 1
        
        self.audit_results['checks'].append(check)
    
    def check_database_security(self):
        """Verifica segurança do banco de dados"""
        check = {
            'name': 'Database Security',
            'status': 'PASS',
            'details': [],
            'score': 0
        }
        
        # Verificar URL do banco
        db_url = os.environ.get('DATABASE_URL')
        if db_url:
            if db_url.startswith('postgresql://'):
                check['details'].append('Usando PostgreSQL (recomendado para produção)')
                check['score'] += 3
            elif db_url.startswith('sqlite://'):
                check['status'] = 'WARN'
                check['details'].append('Usando SQLite (não recomendado para produção)')
                check['score'] += 1
            else:
                check['details'].append('Banco de dados configurado')
                check['score'] += 2
        else:
            check['status'] = 'WARN'
            check['details'].append('DATABASE_URL não configurada')
            check['score'] += 1
        
        # Verificar se não está usando credenciais padrão
        if 'postgresql://' in (db_url or ''):
            if 'postgres:postgres@' in (db_url or ''):
                check['status'] = 'FAIL'
                check['details'].append('Usando credenciais padrão do PostgreSQL')
                check['score'] = 0
            else:
                check['details'].append('Credenciais do banco configuradas')
                check['score'] += 2
        
        self.audit_results['checks'].append(check)
    
    def check_dependencies(self):
        """Verifica dependências de segurança"""
        check = {
            'name': 'Dependencies Security',
            'status': 'PASS',
            'details': [],
            'score': 0
        }
        
        # Verificar se requirements.txt existe
        if Path('requirements.txt').exists():
            check['details'].append('requirements.txt encontrado')
            check['score'] += 1
            
            # Verificar dependências de segurança
            with open('requirements.txt', 'r', encoding='utf-8') as f:
                requirements = f.read()
            
            security_deps = [
                'Flask-WTF', 'Flask-Limiter', 'bleach', 'werkzeug'
            ]
            
            for dep in security_deps:
                if dep in requirements:
                    check['details'].append(f'{dep} incluído')
                    check['score'] += 1
                else:
                    check['status'] = 'WARN'
                    check['details'].append(f'{dep} não encontrado')
        else:
            check['status'] = 'FAIL'
            check['details'].append('requirements.txt não encontrado')
            check['score'] = 0
        
        self.audit_results['checks'].append(check)
    
    def check_headers(self):
        """Verifica headers de segurança"""
        check = {
            'name': 'Security Headers',
            'status': 'PASS',
            'details': [],
            'score': 0
        }
        
        # Verificar se headers estão configurados no código
        if Path('app.py').exists():
            with open('app.py', 'r', encoding='utf-8') as f:
                app_content = f.read()
            
            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection',
                'Strict-Transport-Security'
            ]
            
            for header in security_headers:
                if header in app_content:
                    check['details'].append(f'{header} configurado')
                    check['score'] += 1
                else:
                    check['status'] = 'WARN'
                    check['details'].append(f'{header} não configurado')
        
        self.audit_results['checks'].append(check)
    
    def check_logging(self):
        """Verifica configuração de logging"""
        check = {
            'name': 'Security Logging',
            'status': 'PASS',
            'details': [],
            'score': 0
        }
        
        # Verificar se logging está configurado
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        if log_level in ['INFO', 'WARNING', 'ERROR']:
            check['details'].append(f'Log level configurado: {log_level}')
            check['score'] += 2
        else:
            check['status'] = 'WARN'
            check['details'].append('Log level não configurado adequadamente')
            check['score'] += 1
        
        # Verificar se arquivo de log está configurado
        log_file = os.environ.get('LOG_FILE')
        if log_file:
            check['details'].append(f'Arquivo de log configurado: {log_file}')
            check['score'] += 2
        else:
            check['status'] = 'WARN'
            check['details'].append('Arquivo de log não configurado')
            check['score'] += 1
        
        self.audit_results['checks'].append(check)
    
    def calculate_score(self):
        """Calcula score total de segurança"""
        total_score = 0
        max_score = 0
        
        for check in self.audit_results['checks']:
            total_score += check['score']
            max_score += 5  # Score máximo por categoria
        
        if max_score > 0:
            self.audit_results['score'] = round((total_score / max_score) * 100, 2)
        else:
            self.audit_results['score'] = 0
    
    def generate_report(self):
        """Gera relatório de segurança"""
        score = self.audit_results['score']
        
        if score >= 80:
            status = 'EXCELLENT'
            color = '🟢'
        elif score >= 60:
            status = 'GOOD'
            color = '🟡'
        elif score >= 40:
            status = 'FAIR'
            color = '🟠'
        else:
            status = 'POOR'
            color = '🔴'
        
        self.audit_results['status'] = status
        self.audit_results['color'] = color
        
        # Gerar recomendações
        self.generate_recommendations()
    
    def generate_recommendations(self):
        """Gera recomendações de segurança"""
        recommendations = []
        
        for check in self.audit_results['checks']:
            if check['status'] == 'FAIL':
                recommendations.append(f"[FAIL] {check['name']}: {check['details'][0]}")
            elif check['status'] == 'WARN':
                recommendations.append(f"[WARN] {check['name']}: {check['details'][0]}")
        
        self.audit_results['recommendations'] = recommendations
    
    def print_report(self):
        """Imprime relatório de segurança"""
        print("\n" + "="*60)
        print("RELATORIO DE AUDITORIA DE SEGURANCA")
        print("="*60)
        
        print(f"\nScore de Seguranca: {self.audit_results['score']}%")
        print(f"Status: {self.audit_results['status']}")
        
        print(f"\nVerificacoes Realizadas:")
        for check in self.audit_results['checks']:
            status_icon = "[OK]" if check['status'] == 'PASS' else "[WARN]" if check['status'] == 'WARN' else "[FAIL]"
            print(f"  {status_icon} {check['name']}: {check['status']} (Score: {check['score']}/5)")
            for detail in check['details']:
                print(f"    - {detail}")
        
        if self.audit_results['recommendations']:
            print(f"\nRecomendacoes:")
            for rec in self.audit_results['recommendations']:
                print(f"  {rec}")
        
        print("\n" + "="*60)

def main():
    """Função principal"""
    print("Iniciando auditoria de seguranca do SaaS Sistema...")
    
    audit = SecurityAudit()
    results = audit.run_audit()
    audit.print_report()
    
    # Salvar relatório
    with open('security_audit_report.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nRelatorio salvo em: security_audit_report.json")
    
    # Retornar código de saída baseado no score
    if results['score'] >= 60:
        sys.exit(0)  # Sucesso
    else:
        sys.exit(1)  # Falha

if __name__ == '__main__':
    main()
