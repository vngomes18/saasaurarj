#!/usr/bin/env python3
"""
Validadores de Segurança para SaaS Sistema de Gestão
Implementa validações robustas de entrada e segurança
"""

import re
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Any
import bleach
from werkzeug.security import check_password_hash, generate_password_hash

class SecurityValidators:
    """Classe para validações de segurança"""
    
    # Padrões de validação
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PHONE_PATTERN = re.compile(r'^\+?[\d\s\-\(\)]{10,20}$')
    CPF_PATTERN = re.compile(r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$')
    CNPJ_PATTERN = re.compile(r'^\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}$')
    
    # Caracteres perigosos
    DANGEROUS_CHARS = ['<', '>', '"', "'", '&', '\x00', '\r', '\n']
    SQL_INJECTION_PATTERNS = [
        r'union\s+select', r'select\s+.*\s+from', r'insert\s+into',
        r'update\s+.*\s+set', r'delete\s+from', r'drop\s+table',
        r'create\s+table', r'alter\s+table', r'exec\s*\(', r'execute\s*\(',
        r'sp_', r'xp_', r'--', r'/\*', r'\*/', r'waitfor\s+delay',
        r'benchmark\s*\(', r'sleep\s*\(', r'load_file\s*\(', r'into\s+outfile'
    ]
    
    # XSS patterns
    XSS_PATTERNS = [
        r'<script[^>]*>.*?</script>', r'javascript:', r'on\w+\s*=',
        r'<iframe[^>]*>', r'<object[^>]*>', r'<embed[^>]*>',
        r'<link[^>]*>', r'<meta[^>]*>', r'<style[^>]*>',
        r'expression\s*\(', r'url\s*\(', r'@import'
    ]
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Valida formato de email"""
        if not email:
            return False, "Email é obrigatório"
        
        if len(email) > 254:
            return False, "Email muito longo"
        
        if not SecurityValidators.EMAIL_PATTERN.match(email):
            return False, "Formato de email inválido"
        
        # Verificar domínios suspeitos
        suspicious_domains = ['tempmail.com', '10minutemail.com', 'guerrillamail.com']
        domain = email.split('@')[1].lower()
        if domain in suspicious_domains:
            return False, "Domínio de email não permitido"
        
        return True, "Email válido"
    
    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, str]:
        """Valida força da senha"""
        if not password:
            return False, "Senha é obrigatória"
        
        if len(password) < 8:
            return False, "Senha deve ter pelo menos 8 caracteres"
        
        if len(password) > 128:
            return False, "Senha muito longa"
        
        # Verificar complexidade
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in password)
        
        if not has_upper:
            return False, "Senha deve conter pelo menos uma letra maiúscula"
        
        if not has_lower:
            return False, "Senha deve conter pelo menos uma letra minúscula"
        
        if not has_digit:
            return False, "Senha deve conter pelo menos um número"
        
        if not has_special:
            return False, "Senha deve conter pelo menos um caractere especial"
        
        # Verificar senhas comuns
        common_passwords = [
            'password', '123456', '123456789', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey'
        ]
        
        if password.lower() in common_passwords:
            return False, "Senha muito comum, escolha uma mais segura"
        
        # Verificar padrões repetitivos
        if len(set(password)) < 4:
            return False, "Senha muito simples, use caracteres mais diversos"
        
        return True, "Senha válida"
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """Valida formato de telefone"""
        if not phone:
            return True, "Telefone é opcional"
        
        # Remover caracteres não numéricos
        clean_phone = re.sub(r'[^\d]', '', phone)
        
        if len(clean_phone) < 10:
            return False, "Telefone deve ter pelo menos 10 dígitos"
        
        if len(clean_phone) > 15:
            return False, "Telefone muito longo"
        
        return True, "Telefone válido"
    
    @staticmethod
    def validate_cpf(cpf: str) -> Tuple[bool, str]:
        """Valida CPF brasileiro"""
        if not cpf:
            return True, "CPF é opcional"
        
        # Remover caracteres não numéricos
        cpf = re.sub(r'[^\d]', '', cpf)
        
        if len(cpf) != 11:
            return False, "CPF deve ter 11 dígitos"
        
        # Verificar se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False, "CPF inválido"
        
        # Calcular dígitos verificadores
        def calculate_digit(cpf_digits, weights):
            total = sum(int(digit) * weight for digit, weight in zip(cpf_digits, weights))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder
        
        # Primeiro dígito
        weights1 = list(range(10, 1, -1))
        digit1 = calculate_digit(cpf[:9], weights1)
        
        # Segundo dígito
        weights2 = list(range(11, 1, -1))
        digit2 = calculate_digit(cpf[:10], weights2)
        
        if cpf[9] != str(digit1) or cpf[10] != str(digit2):
            return False, "CPF inválido"
        
        return True, "CPF válido"
    
    @staticmethod
    def validate_cnpj(cnpj: str) -> Tuple[bool, str]:
        """Valida CNPJ brasileiro"""
        if not cnpj:
            return True, "CNPJ é opcional"
        
        # Remover caracteres não numéricos
        cnpj = re.sub(r'[^\d]', '', cnpj)
        
        if len(cnpj) != 14:
            return False, "CNPJ deve ter 14 dígitos"
        
        # Verificar se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            return False, "CNPJ inválido"
        
        # Calcular dígitos verificadores
        def calculate_digit(cnpj_digits, weights):
            total = sum(int(digit) * weight for digit, weight in zip(cnpj_digits, weights))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder
        
        # Primeiro dígito
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        digit1 = calculate_digit(cnpj[:12], weights1)
        
        # Segundo dígito
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        digit2 = calculate_digit(cnpj[:13], weights2)
        
        if cnpj[12] != str(digit1) or cnpj[13] != str(digit2):
            return False, "CNPJ inválido"
        
        return True, "CNPJ válido"
    
    @staticmethod
    def sanitize_input(text: str, max_length: int = 1000) -> str:
        """Sanitiza entrada de texto"""
        if not text:
            return ""
        
        # Limitar tamanho
        if len(text) > max_length:
            text = text[:max_length]
        
        # Remover caracteres perigosos
        for char in SecurityValidators.DANGEROUS_CHARS:
            text = text.replace(char, '')
        
        # Sanitizar HTML
        text = bleach.clean(text, tags=[], strip=True)
        
        return text.strip()
    
    @staticmethod
    def detect_sql_injection(text: str) -> bool:
        """Detecta tentativas de SQL injection"""
        if not text:
            return False
        
        text_lower = text.lower()
        
        for pattern in SecurityValidators.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        
        return False
    
    @staticmethod
    def detect_xss(text: str) -> bool:
        """Detecta tentativas de XSS"""
        if not text:
            return False
        
        for pattern in SecurityValidators.XSS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    @staticmethod
    def validate_file_upload(filename: str, content_type: str, max_size: int = 16777216) -> Tuple[bool, str]:
        """Valida upload de arquivo"""
        if not filename:
            return False, "Nome do arquivo é obrigatório"
        
        # Verificar extensão
        allowed_extensions = {'.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.csv', '.xlsx', '.doc', '.docx'}
        file_ext = '.' + filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext not in allowed_extensions:
            return False, f"Tipo de arquivo não permitido: {file_ext}"
        
        # Verificar tipo MIME
        allowed_mimes = {
            'text/plain', 'application/pdf', 'image/png', 'image/jpeg', 'image/gif',
            'text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }
        
        if content_type not in allowed_mimes:
            return False, f"Tipo MIME não permitido: {content_type}"
        
        # Verificar tamanho (será verificado no upload real)
        return True, "Arquivo válido"
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Gera token seguro"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_password_secure(password: str) -> str:
        """Hash seguro de senha"""
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    
    @staticmethod
    def verify_password_secure(password: str, password_hash: str) -> bool:
        """Verifica senha com hash seguro"""
        return check_password_hash(password_hash, password)
    
    @staticmethod
    def validate_json_input(data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """Valida entrada JSON"""
        if not isinstance(data, dict):
            return False, "Dados devem ser um objeto JSON", {}
        
        # Limitar profundidade
        def check_depth(obj, depth=0, max_depth=10):
            if depth > max_depth:
                return False
            if isinstance(obj, dict):
                return all(check_depth(v, depth + 1, max_depth) for v in obj.values())
            elif isinstance(obj, list):
                return all(check_depth(item, depth + 1, max_depth) for item in obj)
            return True
        
        if not check_depth(data):
            return False, "Estrutura JSON muito profunda", {}
        
        # Sanitizar valores
        sanitized_data = SecurityValidators._sanitize_dict(data)
        
        return True, "JSON válido", sanitized_data
    
    @staticmethod
    def _sanitize_dict(data: Any) -> Any:
        """Sanitiza dicionário recursivamente"""
        if isinstance(data, dict):
            return {key: SecurityValidators._sanitize_dict(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [SecurityValidators._sanitize_dict(item) for item in data]
        elif isinstance(data, str):
            return SecurityValidators.sanitize_input(data)
        else:
            return data
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, str]:
        """Valida URL"""
        if not url:
            return True, "URL é opcional"
        
        # Padrão básico de URL
        url_pattern = re.compile(
            r'^https?://'  # http ou https
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domínio
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # porta opcional
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(url):
            return False, "URL inválida"
        
        # Verificar protocolos seguros
        if not url.startswith(('http://', 'https://')):
            return False, "URL deve usar protocolo HTTP ou HTTPS"
        
        return True, "URL válida"
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
        """Valida intervalo de datas"""
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            if start > end:
                return False, "Data de início deve ser anterior à data de fim"
            
            # Verificar se não é muito antigo (mais de 10 anos)
            if start < datetime.now() - timedelta(days=3650):
                return False, "Data muito antiga"
            
            # Verificar se não é no futuro (mais de 1 ano)
            if end > datetime.now() + timedelta(days=365):
                return False, "Data muito futura"
            
            return True, "Intervalo de datas válido"
        
        except ValueError:
            return False, "Formato de data inválido (use YYYY-MM-DD)"
    
    @staticmethod
    def validate_numeric_range(value: float, min_val: float = None, max_val: float = None) -> Tuple[bool, str]:
        """Valida valor numérico em um intervalo"""
        if min_val is not None and value < min_val:
            return False, f"Valor deve ser maior ou igual a {min_val}"
        
        if max_val is not None and value > max_val:
            return False, f"Valor deve ser menor ou igual a {max_val}"
        
        return True, "Valor numérico válido"
    
    @staticmethod
    def validate_string_length(text: str, min_length: int = 0, max_length: int = 1000) -> Tuple[bool, str]:
        """Valida comprimento de string"""
        if len(text) < min_length:
            return False, f"Texto deve ter pelo menos {min_length} caracteres"
        
        if len(text) > max_length:
            return False, f"Texto deve ter no máximo {max_length} caracteres"
        
        return True, "Comprimento de texto válido"
