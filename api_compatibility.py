
# ========== CAMADA DE COMPATIBILIDADE ==========
"""
Camada de compatibilidade para migração gradual
Mantém endpoints antigos funcionando durante a transição
"""

from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import jwt_required, get_jwt_identity

# Blueprint de compatibilidade
compat_api = Blueprint('compat_api', __name__, url_prefix='/api/compat')

@compat_api.route('/produtos')
def compat_produtos():
    """Endpoint de compatibilidade para produtos"""
    # Redirecionar para nova API
    from api_unified import api_produtos
    return api_produtos()

@compat_api.route('/clientes')
def compat_clientes():
    """Endpoint de compatibilidade para clientes"""
    # Redirecionar para nova API
    from api_unified import api_clientes
    return api_clientes()

@compat_api.route('/dashboard')
def compat_dashboard():
    """Endpoint de compatibilidade para dashboard"""
    # Redirecionar para nova API
    from api_unified import api_dashboard
    return api_dashboard()
