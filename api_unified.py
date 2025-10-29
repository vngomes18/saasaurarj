# ========== API UNIFICADA PARA REACT FRONTEND ==========
"""
API Router unificado com autenticação consistente e estrutura organizada
Resolve duplicações e padroniza autenticação
"""

from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import datetime, timedelta
import json

# Criar blueprint unificado para API
api = Blueprint('api', __name__, url_prefix='/api')

# ========== DECORATORS DE AUTENTICAÇÃO UNIFICADOS ==========

def require_auth(f):
    """Decorator unificado para autenticação (sessão ou JWT)"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar se é JWT (mobile) ou sessão (web)
        if request.headers.get('Authorization'):
            # Usar JWT para mobile
            try:
                from flask_jwt_extended import verify_jwt_in_request
                verify_jwt_in_request()
                return f(*args, **kwargs)
            except Exception:
                return jsonify({
                    'success': False,
                    'error': 'Token JWT inválido'
                }), 401
        else:
            # Usar sessão para web
            if 'user_id' not in session:
                return jsonify({
                    'success': False,
                    'error': 'Não autenticado'
                }), 401
            return f(*args, **kwargs)
    
    return decorated_function

def get_current_user_id():
    """Obtém o ID do usuário atual (sessão ou JWT)"""
    if request.headers.get('Authorization'):
        # JWT para mobile
        return get_jwt_identity()
    else:
        # Sessão para web
        return session.get('user_id')

# ========== DASHBOARD API ==========
@api.route('/dashboard')
@require_auth
def api_dashboard():
    """API endpoint para dados do dashboard"""
    from app import db
    from app import User, Produto, Cliente, Fornecedor, Venda, Compra, ProdutoAuxiliar
    
    try:
        user_id = get_current_user_id()
        
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
@api.route('/produtos', methods=['GET', 'POST'])
@require_auth
def api_produtos():
    """API endpoint para CRUD de produtos"""
    from app import db
    from app import Produto
    
    try:
        user_id = get_current_user_id()
        
        if request.method == 'GET':
            # Listar produtos
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
        
        elif request.method == 'POST':
            # Criar produto
            data = request.get_json()
            
            produto = Produto(
                nome=data.get('nome'),
                descricao=data.get('descricao'),
                preco=float(data.get('preco', 0)),
                estoque_atual=int(data.get('estoque_atual', 0)),
                estoque_minimo=int(data.get('estoque_minimo', 0)),
                categoria=data.get('categoria'),
                codigo_barras=data.get('codigo_barras'),
                user_id=user_id
            )
            
            db.session.add(produto)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': {
                    'id': produto.id,
                    'nome': produto.nome,
                    'message': 'Produto criado com sucesso'
                }
            }), 201
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/produtos/<int:produto_id>', methods=['GET', 'PUT', 'DELETE'])
@require_auth
def api_produto(produto_id):
    """API endpoint para operações específicas de produto"""
    from app import db
    from app import Produto
    
    try:
        user_id = get_current_user_id()
        produto = Produto.query.filter_by(id=produto_id, user_id=user_id).first()
        
        if not produto:
            return jsonify({
                'success': False,
                'error': 'Produto não encontrado'
            }), 404
        
        if request.method == 'GET':
            # Buscar produto específico
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
        
        elif request.method == 'PUT':
            # Atualizar produto
            data = request.get_json()
            
            produto.nome = data.get('nome', produto.nome)
            produto.descricao = data.get('descricao', produto.descricao)
            produto.preco = float(data.get('preco', produto.preco))
            produto.estoque_atual = int(data.get('estoque_atual', produto.estoque_atual))
            produto.estoque_minimo = int(data.get('estoque_minimo', produto.estoque_minimo))
            produto.categoria = data.get('categoria', produto.categoria)
            produto.codigo_barras = data.get('codigo_barras', produto.codigo_barras)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': {
                    'id': produto.id,
                    'nome': produto.nome,
                    'message': 'Produto atualizado com sucesso'
                }
            })
        
        elif request.method == 'DELETE':
            # Deletar produto
            db.session.delete(produto)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Produto deletado com sucesso'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========== CLIENTES API ==========
@api.route('/clientes', methods=['GET', 'POST'])
@require_auth
def api_clientes():
    """API endpoint para CRUD de clientes"""
    from app import db
    from app import Cliente
    
    try:
        user_id = get_current_user_id()
        
        if request.method == 'GET':
            # Listar clientes
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
        
        elif request.method == 'POST':
            # Criar cliente
            data = request.get_json()
            
            cliente = Cliente(
                nome=data.get('nome'),
                email=data.get('email'),
                telefone=data.get('telefone'),
                endereco=data.get('endereco'),
                user_id=user_id
            )
            
            db.session.add(cliente)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': {
                    'id': cliente.id,
                    'nome': cliente.nome,
                    'message': 'Cliente criado com sucesso'
                }
            }), 201
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/clientes/<int:cliente_id>', methods=['GET', 'PUT', 'DELETE'])
@require_auth
def api_cliente(cliente_id):
    """API endpoint para operações específicas de cliente"""
    from app import db
    from app import Cliente
    
    try:
        user_id = get_current_user_id()
        cliente = Cliente.query.filter_by(id=cliente_id, user_id=user_id).first()
        
        if not cliente:
            return jsonify({
                'success': False,
                'error': 'Cliente não encontrado'
            }), 404
        
        if request.method == 'GET':
            # Buscar cliente específico
            return jsonify({
                'success': True,
                'data': {
                    'id': cliente.id,
                    'nome': cliente.nome,
                    'email': cliente.email,
                    'telefone': cliente.telefone,
                    'endereco': cliente.endereco,
                    'created_at': cliente.created_at.isoformat() if cliente.created_at else None
                }
            })
        
        elif request.method == 'PUT':
            # Atualizar cliente
            data = request.get_json()
            
            cliente.nome = data.get('nome', cliente.nome)
            cliente.email = data.get('email', cliente.email)
            cliente.telefone = data.get('telefone', cliente.telefone)
            cliente.endereco = data.get('endereco', cliente.endereco)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': {
                    'id': cliente.id,
                    'nome': cliente.nome,
                    'message': 'Cliente atualizado com sucesso'
                }
            })
        
        elif request.method == 'DELETE':
            # Deletar cliente
            db.session.delete(cliente)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Cliente deletado com sucesso'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========== VENDAS API ==========
@api.route('/vendas', methods=['GET', 'POST'])
@require_auth
def api_vendas():
    """API endpoint para CRUD de vendas"""
    from app import db
    from app import Venda
    
    try:
        user_id = get_current_user_id()
        
        if request.method == 'GET':
            # Listar vendas
            vendas = Venda.query.filter_by(user_id=user_id)\
                .order_by(Venda.data_venda.desc())\
                .all()
            
            return jsonify({
                'success': True,
                'data': [
                    {
                        'id': venda.id,
                        'cliente_id': venda.cliente_id,
                        'cliente_nome': venda.cliente.nome if venda.cliente else 'Cliente não informado',
                        'valor_total': float(venda.valor_total),
                        'valor_final': float(venda.valor_final),
                        'data_venda': venda.data_venda.isoformat(),
                        'status': venda.status,
                        'forma_pagamento': venda.forma_pagamento
                    } for venda in vendas
                ]
            })
        
        elif request.method == 'POST':
            # Criar venda
            data = request.get_json()
            
            venda = Venda(
                cliente_id=data.get('cliente_id'),
                valor_total=float(data.get('valor_total', 0)),
                valor_desconto=float(data.get('valor_desconto', 0)),
                valor_final=float(data.get('valor_final', data.get('valor_total', 0))),
                status=data.get('status', 'finalizada'),
                forma_pagamento=data.get('forma_pagamento', 'dinheiro'),
                observacoes=data.get('observacoes'),
                user_id=user_id
            )
            
            db.session.add(venda)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': {
                    'id': venda.id,
                    'cliente_id': venda.cliente_id,
                    'valor_total': float(venda.valor_total),
                    'valor_final': float(venda.valor_final),
                    'message': 'Venda criada com sucesso'
                }
            }), 201
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========== AUTENTICAÇÃO API ==========
@api.route('/auth/me')
@require_auth
def api_auth_me():
    """API endpoint para informações do usuário logado"""
    from app import db
    from app import User
    
    try:
        user_id = get_current_user_id()
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
@require_auth
def api_stats():
    """API endpoint para estatísticas gerais"""
    from app import db
    from app import Produto, Cliente, Fornecedor, Venda, Compra
    
    try:
        user_id = get_current_user_id()
        
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

# ========== UTILITÁRIOS API ==========
@api.route('/cep/<string:cep>')
def api_cep(cep):
    """API para buscar dados do CEP"""
    import requests
    
    try:
        # Usar API ViaCEP
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        
        if response.status_code == 200:
            data = response.json()
            if 'erro' not in data:
                return jsonify({
                    'success': True,
                    'data': {
                        'cep': data.get('cep'),
                        'logradouro': data.get('logradouro'),
                        'bairro': data.get('bairro'),
                        'localidade': data.get('localidade'),
                        'uf': data.get('uf')
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'CEP não encontrado'
                }), 404
        else:
            return jsonify({
                'success': False,
                'error': 'Erro ao buscar CEP'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
