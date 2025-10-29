# ========== API ROUTES PARA REACT FRONTEND ==========

from flask import Blueprint, jsonify, request, session
from datetime import datetime, timedelta
import json

# Criar blueprint para API
api = Blueprint('api', __name__, url_prefix='/api')

# ========== DASHBOARD API ==========
@api.route('/dashboard')
def api_dashboard():
    """API endpoint para dados do dashboard"""
    # Importações dinâmicas para evitar importação circular
    from app import db
    from models import User, Produto, Cliente, Fornecedor, Venda, Compra, ProdutoAuxiliar
    
    try:
        # Verificar autenticação
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'error': 'Não autenticado'
            }), 401
        
        user_id = session['user_id']
        
        # Buscar dados do dashboard
        total_produtos = Produto.query.filter_by(user_id=user_id).count()
        total_clientes = Cliente.query.filter_by(user_id=user_id).count()
        total_fornecedores = Fornecedor.query.filter_by(user_id=user_id).count()
        total_produtos_auxiliares = ProdutoAuxiliar.query.filter_by(user_id=user_id).count()
        
        # Vendas do mês
        inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        vendas_mes = Venda.query.filter(
            Venda.user_id == user_id,
            Venda.data_venda >= inicio_mes
        ).all()
        total_vendas_mes = sum(venda.total for venda in vendas_mes)
        
        # Compras do mês
        compras_mes = Compra.query.filter(
            Compra.user_id == user_id,
            Compra.data_compra >= inicio_mes
        ).all()
        total_compras_mes = sum(compra.total for compra in compras_mes)
        
        # Estoque baixo
        produtos_estoque_baixo = Produto.query.filter(
            Produto.user_id == user_id,
            Produto.estoque_atual <= Produto.estoque_minimo
        ).count()
        
        produtos_auxiliares_estoque_baixo = ProdutoAuxiliar.query.filter(
            ProdutoAuxiliar.user_id == user_id,
            ProdutoAuxiliar.estoque_atual <= ProdutoAuxiliar.estoque_minimo
        ).count()
        
        # Vendas dos últimos 7 dias
        data_7_dias_atras = datetime.now() - timedelta(days=7)
        vendas_7_dias = Venda.query.filter(
            Venda.user_id == user_id,
            Venda.data_venda >= data_7_dias_atras
        ).all()
        
        # Processar dados para gráfico
        vendas_por_dia = {}
        for venda in vendas_7_dias:
            data_str = venda.data_venda.strftime('%Y-%m-%d')
            if data_str not in vendas_por_dia:
                vendas_por_dia[data_str] = 0
            vendas_por_dia[data_str] += float(venda.total)
        
        # Vendas recentes
        vendas_recentes = Venda.query.filter_by(user_id=user_id)\
            .order_by(Venda.data_venda.desc())\
            .limit(5)\
            .all()
        
        return jsonify({
            'success': True,
            'data': {
                'total_produtos': total_produtos,
                'total_clientes': total_clientes,
                'total_fornecedores': total_fornecedores,
                'total_produtos_auxiliares': total_produtos_auxiliares,
                'total_vendas_mes': total_vendas_mes,
                'total_compras_mes': total_compras_mes,
                'produtos_estoque_baixo': produtos_estoque_baixo,
                'produtos_auxiliares_estoque_baixo': produtos_auxiliares_estoque_baixo,
                'vendas_7_dias': vendas_por_dia,
                'vendas_recentes': [
                    {
                        'id': venda.id,
                        'cliente_nome': venda.cliente_nome,
                        'total': float(venda.total),
                        'data_venda': venda.data_venda.isoformat(),
                        'status': venda.status
                    } for venda in vendas_recentes
                ]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========== PRODUTOS API ==========
@api.route('/produtos')
def api_produtos():
    """API endpoint para listar produtos"""
    # Importações dinâmicas para evitar importação circular
    from app import db
    from models import Produto
    
    try:
        # Verificar autenticação
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'error': 'Não autenticado'
            }), 401
        
        user_id = session['user_id']
        produtos = Produto.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'success': True,
            'data': [
                {
                    'id': produto.id,
                    'nome': produto.nome,
                    'descricao': produto.descricao,
                    'preco': float(produto.preco),
                    'estoque_atual': produto.estoque_atual,
                    'estoque_minimo': produto.estoque_minimo,
                    'categoria': produto.categoria,
                    'codigo_barras': produto.codigo_barras,
                    'created_at': produto.created_at.isoformat() if produto.created_at else None
                } for produto in produtos
            ]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/produtos/<int:produto_id>')
def api_produto(produto_id):
    """API endpoint para produto específico"""
    # Importações dinâmicas para evitar importação circular
    from app import db
    from models import Produto
    
    try:
        # Verificar autenticação
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'error': 'Não autenticado'
            }), 401
        
        user_id = session['user_id']
        produto = Produto.query.filter_by(id=produto_id, user_id=user_id).first()
        
        if not produto:
            return jsonify({
                'success': False,
                'error': 'Produto não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': produto.id,
                'nome': produto.nome,
                'descricao': produto.descricao,
                'preco': float(produto.preco),
                'estoque_atual': produto.estoque_atual,
                'estoque_minimo': produto.estoque_minimo,
                'categoria': produto.categoria,
                'codigo_barras': produto.codigo_barras,
                'created_at': produto.created_at.isoformat() if produto.created_at else None
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========== CLIENTES API ==========
@api.route('/clientes')
def api_clientes():
    """API endpoint para listar clientes"""
    # Importações dinâmicas para evitar importação circular
    from app import db
    from models import Cliente
    
    try:
        # Verificar autenticação
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'error': 'Não autenticado'
            }), 401
        
        user_id = session['user_id']
        clientes = Cliente.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'success': True,
            'data': [
                {
                    'id': cliente.id,
                    'nome': cliente.nome,
                    'email': cliente.email,
                    'telefone': cliente.telefone,
                    'endereco': cliente.endereco,
                    'created_at': cliente.created_at.isoformat() if cliente.created_at else None
                } for cliente in clientes
            ]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========== VENDAS API ==========
@api.route('/vendas')
def api_vendas():
    """API endpoint para listar vendas"""
    # Importações dinâmicas para evitar importação circular
    from app import db
    from models import Venda
    
    try:
        # Verificar autenticação
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'error': 'Não autenticado'
            }), 401
        
        user_id = session['user_id']
        vendas = Venda.query.filter_by(user_id=user_id)\
            .order_by(Venda.data_venda.desc())\
            .all()
        
        return jsonify({
            'success': True,
            'data': [
                {
                    'id': venda.id,
                    'cliente_nome': venda.cliente_nome,
                    'total': float(venda.total),
                    'data_venda': venda.data_venda.isoformat(),
                    'status': venda.status,
                    'forma_pagamento': venda.forma_pagamento
                } for venda in vendas
            ]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========== AUTENTICAÇÃO API ==========
@api.route('/auth/me')
def api_auth_me():
    """API endpoint para informações do usuário logado"""
    # Importações dinâmicas para evitar importação circular
    from app import db
    from models import User
    
    try:
        # Verificar autenticação
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'error': 'Não autenticado'
            }), 401
        
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuário não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'empresa': user.empresa,
                'role': user.role
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========== ESTATÍSTICAS API ==========
@api.route('/stats')
def api_stats():
    """API endpoint para estatísticas gerais"""
    # Importações dinâmicas para evitar importação circular
    from app import db
    from models import Produto, Cliente, Fornecedor, Venda, Compra
    
    try:
        # Verificar autenticação
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'error': 'Não autenticado'
            }), 401
        
        user_id = session['user_id']
        
        # Estatísticas básicas
        stats = {
            'total_produtos': Produto.query.filter_by(user_id=user_id).count(),
            'total_clientes': Cliente.query.filter_by(user_id=user_id).count(),
            'total_fornecedores': Fornecedor.query.filter_by(user_id=user_id).count(),
            'total_vendas': Venda.query.filter_by(user_id=user_id).count(),
            'total_compras': Compra.query.filter_by(user_id=user_id).count()
        }
        
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
