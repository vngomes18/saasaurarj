from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from functools import wraps
from config import config
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

app = Flask(__name__)

# Configurações
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Decorator para verificar login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Função para obter configurações do usuário
def get_user_settings(user_id):
    settings = UserSettings.query.filter_by(user_id=user_id).first()
    if not settings:
        settings = UserSettings(user_id=user_id)
        db.session.add(settings)
        db.session.commit()
    return settings

# Função para atualizar configurações do usuário
def update_user_settings(user_id, **kwargs):
    settings = get_user_settings(user_id)
    for key, value in kwargs.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
    settings.updated_at = datetime.utcnow()
    db.session.commit()
    return settings

# Modelos do Banco de Dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    empresa = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    produtos = db.relationship('Produto', backref='usuario', lazy=True)
    vendas = db.relationship('Venda', backref='usuario', lazy=True)
    clientes = db.relationship('Cliente', backref='usuario', lazy=True)
    fornecedores = db.relationship('Fornecedor', backref='usuario', lazy=True)
    compras = db.relationship('Compra', backref='usuario', lazy=True)
    produtos_auxiliares = db.relationship('ProdutoAuxiliar', backref='usuario', lazy=True)
    notas_fiscais = db.relationship('NotaFiscal', backref='usuario', lazy=True)
    tickets_suporte = db.relationship('TicketSuporte', backref='usuario', lazy=True)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    estoque_atual = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=0)
    categoria = db.Column(db.String(50))
    codigo_barras = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relacionamentos
    itens_venda = db.relationship('ItemVenda', backref='produto', lazy=True)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.Text)
    cpf_cnpj = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relacionamentos
    vendas = db.relationship('Venda', backref='cliente', lazy=True)

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='finalizada')  # finalizada, cancelada, pendente
    forma_pagamento = db.Column(db.String(30))  # dinheiro, cartao, pix, etc
    observacoes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    
    # Relacionamentos
    itens = db.relationship('ItemVenda', backref='venda', lazy=True, cascade='all, delete-orphan')

class ItemVenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)

# Novos modelos para controle de estoque
class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    razao_social = db.Column(db.String(100))
    cnpj = db.Column(db.String(18))
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.Text)
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(9))
    contato = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='ativo')  # ativo, inativo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relacionamentos
    compras = db.relationship('Compra', backref='fornecedor', lazy=True)

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_compra = db.Column(db.String(50), unique=True)
    data_compra = db.Column(db.DateTime, default=datetime.utcnow)
    data_entrega = db.Column(db.DateTime)
    valor_total = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.String(20), default='pendente')  # pendente, confirmada, entregue, cancelada
    forma_pagamento = db.Column(db.String(30))
    observacoes = db.Column(db.Text)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relacionamentos
    itens = db.relationship('ItemCompra', backref='compra', lazy=True, cascade='all, delete-orphan')
    notas_fiscais = db.relationship('NotaFiscal', backref='compra', lazy=True)

class ItemCompra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)

class ProdutoAuxiliar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(50))
    unidade = db.Column(db.String(20))  # kg, litros, metros, etc
    preco_unitario = db.Column(db.Float, nullable=False)
    estoque_atual = db.Column(db.Float, default=0)
    estoque_minimo = db.Column(db.Float, default=0)
    codigo_interno = db.Column(db.String(50))
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='ativo')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class NotaFiscal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_nf = db.Column(db.String(50), nullable=False)
    serie = db.Column(db.String(10))
    modelo = db.Column(db.String(10), default='NFe')  # NFe, NFCe, etc
    chave_acesso = db.Column(db.String(50))
    data_emissao = db.Column(db.DateTime, default=datetime.utcnow)
    data_saida = db.Column(db.DateTime)
    valor_total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pendente')  # pendente, emitida, cancelada
    tipo_operacao = db.Column(db.String(20))  # entrada, saida
    cliente_fornecedor = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class TicketSuporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(50))  # bug, melhoria, duvida, etc
    prioridade = db.Column(db.String(20), default='media')  # baixa, media, alta, urgente
    status = db.Column(db.String(20), default='aberto')  # aberto, em_andamento, resolvido, fechado
    data_abertura = db.Column(db.DateTime, default=datetime.utcnow)
    data_fechamento = db.Column(db.DateTime)
    anexos = db.Column(db.Text)  # JSON com paths dos anexos
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relacionamentos
    respostas = db.relationship('RespostaTicket', backref='ticket', lazy=True, cascade='all, delete-orphan')

class RespostaTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mensagem = db.Column(db.Text, nullable=False)
    data_resposta = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket_suporte.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dark_mode = db.Column(db.Boolean, default=False)
    notifications = db.Column(db.Boolean, default=True)
    auto_logout = db.Column(db.Integer, default=30)  # minutes
    language = db.Column(db.String(5), default='pt')
    timezone = db.Column(db.String(50), default='America/Sao_Paulo')
    dashboard_refresh = db.Column(db.Integer, default=30)  # seconds
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Rotas de Autenticação
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['empresa'] = user.empresa
            
            # Carregar configurações do usuário
            settings = get_user_settings(user.id)
            session['dark_mode'] = settings.dark_mode
            
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha incorretos!', 'error')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        empresa = request.form['empresa']
        
        # Verificar se usuário já existe por username
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já cadastrado!', 'error')
            return render_template('auth/register.html')
        
        # Verificar se usuário já existe por email
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'error')
            return render_template('auth/register.html')
        
        try:
            # Criar novo usuário
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                empresa=empresa
            )
            
            db.session.add(user)
            db.session.commit()
            
            flash('Conta criada com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar conta. Tente novamente.', 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    
    # Estatísticas básicas
    total_produtos = Produto.query.filter_by(user_id=user_id).count()
    total_clientes = Cliente.query.filter_by(user_id=user_id).count()
    total_fornecedores = Fornecedor.query.filter_by(user_id=user_id, status='ativo').count()
    total_produtos_auxiliares = ProdutoAuxiliar.query.filter_by(user_id=user_id, status='ativo').count()
    
    # Vendas do mês atual
    inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    vendas_mes = Venda.query.filter(
        Venda.user_id == user_id,
        Venda.data_venda >= inicio_mes,
        Venda.status == 'finalizada'
    ).all()
    
    total_vendas_mes = sum(venda.valor_total for venda in vendas_mes)
    
    # Compras do mês atual
    compras_mes = Compra.query.filter(
        Compra.user_id == user_id,
        Compra.data_compra >= inicio_mes
    ).all()
    
    total_compras_mes = sum(compra.valor_total for compra in compras_mes)
    
    # Produtos com estoque baixo
    produtos_estoque_baixo = Produto.query.filter(
        Produto.user_id == user_id,
        Produto.estoque_atual <= Produto.estoque_minimo
    ).count()
    
    # Produtos auxiliares com estoque baixo
    produtos_auxiliares_estoque_baixo = ProdutoAuxiliar.query.filter(
        ProdutoAuxiliar.user_id == user_id,
        ProdutoAuxiliar.estoque_atual <= ProdutoAuxiliar.estoque_minimo
    ).count()
    
    # Tickets de suporte abertos
    tickets_abertos = TicketSuporte.query.filter(
        TicketSuporte.user_id == user_id,
        TicketSuporte.status.in_(['aberto', 'em_andamento'])
    ).count()
    
    # Vendas recentes
    vendas_recentes = Venda.query.filter_by(user_id=user_id).order_by(Venda.data_venda.desc()).limit(5).all()
    
    # Gráfico de vendas dos últimos 7 dias
    vendas_7_dias = []
    for i in range(7):
        data = datetime.now().date() - timedelta(days=i)
        vendas_dia = Venda.query.filter(
            Venda.user_id == user_id,
            db.func.date(Venda.data_venda) == data,
            Venda.status == 'finalizada'
        ).count()
        vendas_7_dias.append({'data': data.strftime('%d/%m'), 'vendas': vendas_dia})
    
    vendas_7_dias.reverse()
    
    return render_template('dashboard.html',
                         total_produtos=total_produtos,
                         total_clientes=total_clientes,
                         total_fornecedores=total_fornecedores,
                         total_produtos_auxiliares=total_produtos_auxiliares,
                         total_vendas_mes=total_vendas_mes,
                         total_compras_mes=total_compras_mes,
                         produtos_estoque_baixo=produtos_estoque_baixo,
                         produtos_auxiliares_estoque_baixo=produtos_auxiliares_estoque_baixo,
                         tickets_abertos=tickets_abertos,
                         vendas_recentes=vendas_recentes,
                         vendas_7_dias=vendas_7_dias)

# Produtos
@app.route('/produtos')
@login_required
def produtos():
    user_id = session['user_id']
    produtos = Produto.query.filter_by(user_id=user_id).order_by(Produto.nome).all()
    return render_template('produtos/list.html', produtos=produtos)

@app.route('/produtos/novo', methods=['GET', 'POST'])
@login_required
def novo_produto():
    if request.method == 'POST':
        # Convert price from Brazilian format (comma) to float
        preco_str = request.form['preco'].replace(',', '.')
        
        produto = Produto(
            nome=request.form['nome'],
            descricao=request.form['descricao'],
            preco=float(preco_str),
            estoque_atual=int(request.form['estoque_atual']),
            estoque_minimo=int(request.form['estoque_minimo']),
            categoria=request.form['categoria'],
            codigo_barras=request.form['codigo_barras'],
            user_id=session['user_id']
        )
        
        db.session.add(produto)
        db.session.commit()
        
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('produtos'))
    
    return render_template('produtos/form.html')

@app.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    produto = Produto.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    
    if request.method == 'POST':
        # Convert price from Brazilian format (comma) to float
        preco_str = request.form['preco'].replace(',', '.')
        
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.preco = float(preco_str)
        produto.estoque_atual = int(request.form['estoque_atual'])
        produto.estoque_minimo = int(request.form['estoque_minimo'])
        produto.categoria = request.form['categoria']
        produto.codigo_barras = request.form['codigo_barras']
        
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('produtos'))
    
    return render_template('produtos/form.html', produto=produto)

@app.route('/produtos/excluir/<int:id>')
@login_required
def excluir_produto(id):
    produto = Produto.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    db.session.delete(produto)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('produtos'))

# Clientes
@app.route('/clientes')
@login_required
def clientes():
    user_id = session['user_id']
    clientes = Cliente.query.filter_by(user_id=user_id).order_by(Cliente.nome).all()
    return render_template('clientes/list.html', clientes=clientes)

@app.route('/clientes/novo', methods=['GET', 'POST'])
@login_required
def novo_cliente():
    if request.method == 'POST':
        cliente = Cliente(
            nome=request.form['nome'],
            email=request.form['email'],
            telefone=request.form['telefone'],
            endereco=request.form['endereco'],
            cpf_cnpj=request.form['cpf_cnpj'],
            user_id=session['user_id']
        )
        
        db.session.add(cliente)
        db.session.commit()
        
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('clientes'))
    
    return render_template('clientes/form.html')

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    cliente = Cliente.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    
    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.email = request.form['email']
        cliente.telefone = request.form['telefone']
        cliente.endereco = request.form['endereco']
        cliente.cpf_cnpj = request.form['cpf_cnpj']
        
        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('clientes'))
    
    return render_template('clientes/form.html', cliente=cliente)

@app.route('/clientes/excluir/<int:id>')
@login_required
def excluir_cliente(id):
    cliente = Cliente.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente excluído com sucesso!', 'success')
    return redirect(url_for('clientes'))

# Vendas
@app.route('/vendas')
@login_required
def vendas():
    user_id = session['user_id']
    vendas = Venda.query.filter_by(user_id=user_id).order_by(Venda.data_venda.desc()).all()
    return render_template('vendas/list.html', vendas=vendas)

@app.route('/vendas/nova', methods=['GET', 'POST'])
@login_required
def nova_venda():
    if request.method == 'POST':
        # Criar venda
        venda = Venda(
            cliente_id=int(request.form['cliente_id']) if request.form['cliente_id'] else None,
            valor_total=0,  # Será calculado
            forma_pagamento=request.form['forma_pagamento'],
            observacoes=request.form['observacoes'],
            user_id=session['user_id']
        )
        
        db.session.add(venda)
        db.session.flush()  # Para obter o ID da venda
        
        # Processar itens da venda
        total_venda = 0
        for key, value in request.form.items():
            if key.startswith('produto_') and value:
                produto_id = key.split('_')[1]
                quantidade = int(value)
                
                produto = Produto.query.filter_by(id=produto_id, user_id=session['user_id']).first()
                if produto and produto.estoque_atual >= quantidade:
                    # Criar item da venda
                    item = ItemVenda(
                        venda_id=venda.id,
                        produto_id=produto.id,
                        quantidade=quantidade,
                        preco_unitario=produto.preco,
                        subtotal=quantidade * produto.preco
                    )
                    
                    db.session.add(item)
                    
                    # Atualizar estoque
                    produto.estoque_atual -= quantidade
                    total_venda += item.subtotal
        
        # Atualizar valor total da venda
        venda.valor_total = total_venda
        
        db.session.commit()
        flash('Venda realizada com sucesso!', 'success')
        return redirect(url_for('vendas'))
    
    user_id = session['user_id']
    produtos = Produto.query.filter_by(user_id=user_id).all()
    clientes = Cliente.query.filter_by(user_id=user_id).all()
    
    return render_template('vendas/form.html', produtos=produtos, clientes=clientes)

@app.route('/vendas/<int:id>')
@login_required
def detalhes_venda(id):
    venda = Venda.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    return render_template('vendas/detalhes.html', venda=venda)

# Rotas de Fornecedores
@app.route('/fornecedores')
@login_required
def fornecedores():
    user_id = session['user_id']
    fornecedores = Fornecedor.query.filter_by(user_id=user_id).order_by(Fornecedor.nome).all()
    return render_template('fornecedores/list.html', fornecedores=fornecedores)

@app.route('/fornecedores/novo', methods=['GET', 'POST'])
@login_required
def novo_fornecedor():
    if request.method == 'POST':
        fornecedor = Fornecedor(
            nome=request.form['nome'],
            razao_social=request.form.get('razao_social'),
            cnpj=request.form.get('cnpj'),
            email=request.form.get('email'),
            telefone=request.form.get('telefone'),
            endereco=request.form.get('endereco'),
            cidade=request.form.get('cidade'),
            estado=request.form.get('estado'),
            cep=request.form.get('cep'),
            contato=request.form.get('contato'),
            observacoes=request.form.get('observacoes'),
            user_id=session['user_id']
        )
        
        db.session.add(fornecedor)
        db.session.commit()
        
        flash('Fornecedor cadastrado com sucesso!', 'success')
        return redirect(url_for('fornecedores'))
    
    return render_template('fornecedores/form.html')

@app.route('/fornecedores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    
    if request.method == 'POST':
        fornecedor.nome = request.form['nome']
        fornecedor.razao_social = request.form.get('razao_social')
        fornecedor.cnpj = request.form.get('cnpj')
        fornecedor.email = request.form.get('email')
        fornecedor.telefone = request.form.get('telefone')
        fornecedor.endereco = request.form.get('endereco')
        fornecedor.cidade = request.form.get('cidade')
        fornecedor.estado = request.form.get('estado')
        fornecedor.cep = request.form.get('cep')
        fornecedor.contato = request.form.get('contato')
        fornecedor.observacoes = request.form.get('observacoes')
        
        db.session.commit()
        flash('Fornecedor atualizado com sucesso!', 'success')
        return redirect(url_for('fornecedores'))
    
    return render_template('fornecedores/form.html', fornecedor=fornecedor)

@app.route('/fornecedores/excluir/<int:id>')
@login_required
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    db.session.delete(fornecedor)
    db.session.commit()
    flash('Fornecedor excluído com sucesso!', 'success')
    return redirect(url_for('fornecedores'))

# Rotas de Compras
@app.route('/compras')
@login_required
def compras():
    user_id = session['user_id']
    compras = Compra.query.filter_by(user_id=user_id).order_by(Compra.data_compra.desc()).all()
    return render_template('compras/list.html', compras=compras)

@app.route('/compras/nova', methods=['GET', 'POST'])
@login_required
def nova_compra():
    if request.method == 'POST':
        # Gerar número da compra
        ultima_compra = Compra.query.filter_by(user_id=session['user_id']).order_by(Compra.id.desc()).first()
        numero_compra = f"COMP{datetime.now().strftime('%Y%m%d')}{(ultima_compra.id + 1 if ultima_compra else 1):04d}"
        
        # Criar compra
        compra = Compra(
            numero_compra=numero_compra,
            fornecedor_id=int(request.form['fornecedor_id']),
            data_entrega=datetime.strptime(request.form['data_entrega'], '%Y-%m-%d') if request.form.get('data_entrega') else None,
            forma_pagamento=request.form.get('forma_pagamento'),
            observacoes=request.form.get('observacoes'),
            user_id=session['user_id']
        )
        
        db.session.add(compra)
        db.session.flush()
        
        # Processar itens da compra
        total_compra = 0
        for key, value in request.form.items():
            if key.startswith('produto_') and value:
                produto_id = key.split('_')[1]
                quantidade = int(value)
                
                produto = Produto.query.filter_by(id=produto_id, user_id=session['user_id']).first()
                if produto:
                    # Criar item da compra
                    item = ItemCompra(
                        compra_id=compra.id,
                        produto_id=produto.id,
                        quantidade=quantidade,
                        preco_unitario=produto.preco,
                        subtotal=quantidade * produto.preco
                    )
                    
                    db.session.add(item)
                    total_compra += item.subtotal
        
        # Atualizar valor total da compra
        compra.valor_total = total_compra
        
        db.session.commit()
        flash('Compra cadastrada com sucesso!', 'success')
        return redirect(url_for('compras'))
    
    user_id = session['user_id']
    produtos = Produto.query.filter_by(user_id=user_id).all()
    fornecedores = Fornecedor.query.filter_by(user_id=user_id, status='ativo').all()
    
    return render_template('compras/form.html', produtos=produtos, fornecedores=fornecedores)

@app.route('/compras/<int:id>')
@login_required
def detalhes_compra(id):
    compra = Compra.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    return render_template('compras/detalhes.html', compra=compra)

@app.route('/compras/confirmar/<int:id>')
@login_required
def confirmar_compra(id):
    compra = Compra.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    
    if compra.status == 'pendente':
        # Atualizar estoque dos produtos
        for item in compra.itens:
            item.produto.estoque_atual += item.quantidade
        
        compra.status = 'confirmada'
        db.session.commit()
        flash('Compra confirmada e estoque atualizado!', 'success')
    
    return redirect(url_for('compras'))

# Rotas de Produtos Auxiliares
@app.route('/produtos-auxiliares')
@login_required
def produtos_auxiliares():
    user_id = session['user_id']
    produtos = ProdutoAuxiliar.query.filter_by(user_id=user_id).order_by(ProdutoAuxiliar.nome).all()
    return render_template('produtos_auxiliares/list.html', produtos=produtos)

@app.route('/produtos-auxiliares/novo', methods=['GET', 'POST'])
@login_required
def novo_produto_auxiliar():
    if request.method == 'POST':
        try:
            # Debug: imprimir dados do formulário
            print("Dados do formulário:", request.form.to_dict())
            
            # Validar campos obrigatórios
            if not request.form.get('nome'):
                flash('Nome do produto é obrigatório!', 'error')
                return render_template('produtos_auxiliares/form.html')
            
            if not request.form.get('preco_unitario'):
                flash('Preço unitário é obrigatório!', 'error')
                return render_template('produtos_auxiliares/form.html')
            
            # Converter valores com tratamento de erro
            preco_unitario = 0.0
            estoque_atual = 0.0
            estoque_minimo = 0.0
            
            try:
                preco_unitario = float(request.form['preco_unitario'])
            except (ValueError, TypeError):
                preco_unitario = 0.0
            
            try:
                estoque_atual = float(request.form.get('estoque_atual', 0))
            except (ValueError, TypeError):
                estoque_atual = 0.0
            
            try:
                estoque_minimo = float(request.form.get('estoque_minimo', 0))
            except (ValueError, TypeError):
                estoque_minimo = 0.0
            
            produto = ProdutoAuxiliar(
                nome=request.form['nome'].strip(),
                descricao=request.form.get('descricao', '').strip(),
                categoria=request.form.get('categoria', '').strip(),
                unidade=request.form.get('unidade', '').strip(),
                preco_unitario=preco_unitario,
                estoque_atual=estoque_atual,
                estoque_minimo=estoque_minimo,
                codigo_interno=request.form.get('codigo_interno', '').strip(),
                observacoes=request.form.get('observacoes', '').strip(),
                user_id=session['user_id']
            )
            
            print("Produto criado:", produto.nome, produto.preco_unitario)
            
            db.session.add(produto)
            db.session.commit()
            
            flash('Produto auxiliar cadastrado com sucesso!', 'success')
            return redirect(url_for('produtos_auxiliares'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao cadastrar produto auxiliar: {str(e)}")
            flash(f'Erro ao cadastrar produto auxiliar: {str(e)}', 'error')
            return render_template('produtos_auxiliares/form.html')
    
    return render_template('produtos_auxiliares/form.html')

@app.route('/produtos-auxiliares/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_produto_auxiliar(id):
    produto = ProdutoAuxiliar.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.descricao = request.form.get('descricao')
        produto.categoria = request.form.get('categoria')
        produto.unidade = request.form.get('unidade')
        produto.preco_unitario = float(request.form['preco_unitario'])
        produto.estoque_atual = float(request.form['estoque_atual'])
        produto.estoque_minimo = float(request.form['estoque_minimo'])
        produto.codigo_interno = request.form.get('codigo_interno')
        produto.observacoes = request.form.get('observacoes')
        
        db.session.commit()
        flash('Produto auxiliar atualizado com sucesso!', 'success')
        return redirect(url_for('produtos_auxiliares'))
    
    return render_template('produtos_auxiliares/form.html', produto=produto)

@app.route('/produtos-auxiliares/excluir/<int:id>')
@login_required
def excluir_produto_auxiliar(id):
    produto = ProdutoAuxiliar.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    db.session.delete(produto)
    db.session.commit()
    flash('Produto auxiliar excluído com sucesso!', 'success')
    return redirect(url_for('produtos_auxiliares'))

# Rotas de Nota Fiscal
@app.route('/notas-fiscais')
@login_required
def notas_fiscais():
    user_id = session['user_id']
    notas = NotaFiscal.query.filter_by(user_id=user_id).order_by(NotaFiscal.data_emissao.desc()).all()
    return render_template('notas_fiscais/list.html', notas=notas)

@app.route('/notas-fiscais/nova', methods=['GET', 'POST'])
@login_required
def nova_nota_fiscal():
    if request.method == 'POST':
        nota = NotaFiscal(
            numero_nf=request.form['numero_nf'],
            serie=request.form.get('serie'),
            modelo=request.form.get('modelo', 'NFe'),
            chave_acesso=request.form.get('chave_acesso'),
            data_saida=datetime.strptime(request.form['data_saida'], '%Y-%m-%d') if request.form.get('data_saida') else None,
            valor_total=float(request.form['valor_total']),
            tipo_operacao=request.form.get('tipo_operacao'),
            cliente_fornecedor=request.form.get('cliente_fornecedor'),
            observacoes=request.form.get('observacoes'),
            compra_id=int(request.form['compra_id']) if request.form.get('compra_id') else None,
            user_id=session['user_id']
        )
        
        db.session.add(nota)
        db.session.commit()
        
        flash('Nota fiscal cadastrada com sucesso!', 'success')
        return redirect(url_for('notas_fiscais'))
    
    user_id = session['user_id']
    compras = Compra.query.filter_by(user_id=user_id).all()
    
    return render_template('notas_fiscais/form.html', compras=compras)

@app.route('/notas-fiscais/<int:id>')
@login_required
def detalhes_nota_fiscal(id):
    nota = NotaFiscal.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    return render_template('notas_fiscais/detalhes.html', nota=nota)

# Rotas de Suporte
@app.route('/suporte')
@login_required
def suporte():
    user_id = session['user_id']
    tickets = TicketSuporte.query.filter_by(user_id=user_id).order_by(TicketSuporte.data_abertura.desc()).all()
    return render_template('suporte/list.html', tickets=tickets)

@app.route('/suporte/novo', methods=['GET', 'POST'])
@login_required
def novo_ticket():
    if request.method == 'POST':
        ticket = TicketSuporte(
            titulo=request.form['titulo'],
            descricao=request.form['descricao'],
            categoria=request.form.get('categoria'),
            prioridade=request.form.get('prioridade', 'media'),
            user_id=session['user_id']
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        flash('Ticket de suporte criado com sucesso!', 'success')
        return redirect(url_for('suporte'))
    
    return render_template('suporte/form.html')

@app.route('/suporte/<int:id>')
@login_required
def detalhes_ticket(id):
    ticket = TicketSuporte.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    return render_template('suporte/detalhes.html', ticket=ticket)

@app.route('/suporte/<int:id>/responder', methods=['POST'])
@login_required
def responder_ticket(id):
    ticket = TicketSuporte.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    
    resposta = RespostaTicket(
        mensagem=request.form['mensagem'],
        ticket_id=ticket.id,
        user_id=session['user_id']
    )
    
    db.session.add(resposta)
    
    # Atualizar status do ticket se necessário
    if ticket.status == 'resolvido':
        ticket.status = 'aberto'
    
    db.session.commit()
    flash('Resposta enviada com sucesso!', 'success')
    return redirect(url_for('detalhes_ticket', id=id))

# API para buscar produtos
@app.route('/api/produtos')
@login_required
def api_produtos():
    user_id = session['user_id']
    produtos = Produto.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': p.id,
        'nome': p.nome,
        'preco': p.preco,
        'estoque_atual': p.estoque_atual
    } for p in produtos])

# API para buscar fornecedores
@app.route('/api/fornecedores')
@login_required
def api_fornecedores():
    user_id = session['user_id']
    fornecedores = Fornecedor.query.filter_by(user_id=user_id, status='ativo').all()
    
    return jsonify([{
        'id': f.id,
        'nome': f.nome,
        'razao_social': f.razao_social,
        'cnpj': f.cnpj
    } for f in fornecedores])

# Rotas de Configurações
@app.route('/configuracoes')
@login_required
def configuracoes():
    user_id = session['user_id']
    settings = get_user_settings(user_id)
    return render_template('configuracoes/index.html', settings=settings)

@app.route('/configuracoes/atualizar', methods=['POST'])
@login_required
def atualizar_configuracoes():
    user_id = session['user_id']
    
    # Processar dados do formulário
    dark_mode = request.form.get('dark_mode') == 'on'
    notifications = request.form.get('notifications') == 'on'
    auto_logout = int(request.form.get('auto_logout', 30))
    language = request.form.get('language', 'pt')
    timezone = request.form.get('timezone', 'America/Sao_Paulo')
    dashboard_refresh = int(request.form.get('dashboard_refresh', 30))
    
    # Debug: imprimir valores recebidos
    print(f"Dark mode received: {request.form.get('dark_mode')}")
    print(f"Dark mode processed: {dark_mode}")
    print(f"User ID: {user_id}")
    
    # Atualizar configurações
    update_user_settings(user_id,
                        dark_mode=dark_mode,
                        notifications=notifications,
                        auto_logout=auto_logout,
                        language=language,
                        timezone=timezone,
                        dashboard_refresh=dashboard_refresh)
    
    # Atualizar sessão
    session['dark_mode'] = dark_mode
    
    flash('Configurações atualizadas com sucesso!', 'success')
    return redirect(url_for('configuracoes'))

@app.route('/api/toggle-dark-mode', methods=['POST'])
@login_required
def toggle_dark_mode():
    user_id = session['user_id']
    settings = get_user_settings(user_id)
    
    # Alternar dark mode
    new_dark_mode = not settings.dark_mode
    update_user_settings(user_id, dark_mode=new_dark_mode)
    
    # Atualizar sessão
    session['dark_mode'] = new_dark_mode
    
    return jsonify({
        'success': True,
        'dark_mode': new_dark_mode,
        'message': 'Modo escuro ' + ('ativado' if new_dark_mode else 'desativado')
    })

# ==================== RELATÓRIOS E ANALYTICS ====================

# Página principal de relatórios
@app.route('/relatorios')
@login_required
def relatorios():
    user_id = session['user_id']
    
    # KPIs rápidos para o dashboard de relatórios
    total_produtos = Produto.query.filter_by(user_id=user_id).count()
    total_clientes = Cliente.query.filter_by(user_id=user_id).count()
    
    # Vendas do mês atual
    inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    vendas_mes = Venda.query.filter(
        Venda.user_id == user_id,
        Venda.data_venda >= inicio_mes,
        Venda.status == 'finalizada'
    ).all()
    
    receita_mes = sum(venda.valor_total for venda in vendas_mes)
    
    # Produtos com estoque baixo
    produtos_estoque_baixo = Produto.query.filter(
        Produto.user_id == user_id,
        Produto.estoque_atual <= Produto.estoque_minimo
    ).count()
    
    return render_template('relatorios/index.html',
                         total_produtos=total_produtos,
                         total_clientes=total_clientes,
                         receita_mes=receita_mes,
                         produtos_estoque_baixo=produtos_estoque_baixo)

# ==================== RELATÓRIOS FINANCEIROS ====================

# P&L (Profit & Loss)
@app.route('/relatorios/pl')
@login_required
def relatorio_pl():
    user_id = session['user_id']
    
    # Período (padrão: mês atual)
    inicio = request.args.get('inicio', datetime.now().replace(day=1).strftime('%Y-%m-%d'))
    fim = request.args.get('fim', datetime.now().strftime('%Y-%m-%d'))
    
    # Receitas
    vendas = Venda.query.filter(
        Venda.user_id == user_id,
        Venda.data_venda.between(inicio, fim),
        Venda.status == 'finalizada'
    ).all()
    
    receita_total = sum(v.valor_total for v in vendas)
    
    # Custos
    compras = Compra.query.filter(
        Compra.user_id == user_id,
        Compra.data_compra.between(inicio, fim)
    ).all()
    
    custo_total = sum(c.valor_total for c in compras)
    
    # Margem de lucro
    margem_lucro = receita_total - custo_total
    margem_percentual = (margem_lucro / receita_total * 100) if receita_total > 0 else 0
    
    return render_template('relatorios/pl.html', 
                         receita_total=receita_total,
                         custo_total=custo_total,
                         margem_lucro=margem_lucro,
                         margem_percentual=margem_percentual,
                         periodo={'inicio': inicio, 'fim': fim})

# Fluxo de Caixa
@app.route('/relatorios/fluxo-caixa')
@login_required
def relatorio_fluxo_caixa():
    user_id = session['user_id']
    
    # Últimos 12 meses
    fluxo_mensal = []
    for i in range(12):
        mes = datetime.now() - timedelta(days=30*i)
        inicio_mes = mes.replace(day=1)
        fim_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Entradas (vendas)
        vendas_mes = Venda.query.filter(
            Venda.user_id == user_id,
            Venda.data_venda.between(inicio_mes, fim_mes),
            Venda.status == 'finalizada'
        ).all()
        
        entradas = sum(v.valor_total for v in vendas_mes)
        
        # Saídas (compras)
        compras_mes = Compra.query.filter(
            Compra.user_id == user_id,
            Compra.data_compra.between(inicio_mes, fim_mes)
        ).all()
        
        saidas = sum(c.valor_total for c in compras_mes)
        
        fluxo_mensal.append({
            'mes': inicio_mes.strftime('%Y-%m'),
            'entradas': entradas,
            'saidas': saidas,
            'saldo': entradas - saidas
        })
    
    return render_template('relatorios/fluxo_caixa.html', fluxo_mensal=fluxo_mensal)

# ==================== ANÁLISE DE VENDAS ====================

# Top Produtos
@app.route('/relatorios/top-produtos')
@login_required
def relatorio_top_produtos():
    user_id = session['user_id']
    
    # Query para produtos mais vendidos
    top_produtos = db.session.query(
        Produto.nome,
        db.func.sum(ItemVenda.quantidade).label('total_vendido'),
        db.func.sum(ItemVenda.quantidade * ItemVenda.preco_unitario).label('receita_total')
    ).join(ItemVenda).join(Venda).filter(
        Venda.user_id == user_id,
        Venda.status == 'finalizada'
    ).group_by(Produto.id, Produto.nome).order_by(
        db.func.sum(ItemVenda.quantidade).desc()
    ).limit(10).all()
    
    return render_template('relatorios/top_produtos.html', top_produtos=top_produtos)

# Análise de Sazonalidade
@app.route('/relatorios/sazonalidade')
@login_required
def relatorio_sazonalidade():
    user_id = session['user_id']
    
    # Vendas por mês (últimos 12 meses)
    vendas_por_mes = []
    for i in range(12):
        mes = datetime.now() - timedelta(days=30*i)
        inicio_mes = mes.replace(day=1)
        fim_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        vendas_mes = Venda.query.filter(
            Venda.user_id == user_id,
            Venda.data_venda.between(inicio_mes, fim_mes),
            Venda.status == 'finalizada'
        ).all()
        
        vendas_por_mes.append({
            'mes': inicio_mes.strftime('%Y-%m'),
            'total': sum(v.valor_total for v in vendas_mes),
            'quantidade': len(vendas_mes)
        })
    
    return render_template('relatorios/sazonalidade.html', vendas_por_mes=vendas_por_mes)

# ==================== RELATÓRIOS DE ESTOQUE ====================

# Rotatividade de Produtos
@app.route('/relatorios/rotatividade-estoque')
@login_required
def relatorio_rotatividade_estoque():
    user_id = session['user_id']
    
    produtos_rotatividade = []
    produtos = Produto.query.filter_by(user_id=user_id).all()
    
    for produto in produtos:
        # Vendas do produto nos últimos 30 dias
        inicio = datetime.now() - timedelta(days=30)
        vendas_produto = db.session.query(
            db.func.sum(ItemVenda.quantidade)
        ).join(Venda).filter(
            ItemVenda.produto_id == produto.id,
            Venda.user_id == user_id,
            Venda.data_venda >= inicio,
            Venda.status == 'finalizada'
        ).scalar() or 0
        
        # Rotatividade = vendas / estoque médio
        estoque_medio = produto.estoque_atual
        rotatividade = (vendas_produto / estoque_medio) if estoque_medio > 0 else 0
        
        produtos_rotatividade.append({
            'produto': produto,
            'vendas_30_dias': vendas_produto,
            'estoque_atual': produto.estoque_atual,
            'rotatividade': rotatividade
        })
    
    # Ordenar por rotatividade
    produtos_rotatividade.sort(key=lambda x: x['rotatividade'], reverse=True)
    
    return render_template('relatorios/rotatividade_estoque.html', 
                         produtos_rotatividade=produtos_rotatividade)

# Produtos Parados
@app.route('/relatorios/produtos-parados')
@login_required
def relatorio_produtos_parados():
    user_id = session['user_id']
    
    # Produtos sem vendas nos últimos 90 dias
    inicio = datetime.now() - timedelta(days=90)
    
    produtos_parados = []
    produtos = Produto.query.filter_by(user_id=user_id).all()
    
    for produto in produtos:
        # Verificar se teve vendas nos últimos 90 dias
        vendas_recentes = db.session.query(ItemVenda).join(Venda).filter(
            ItemVenda.produto_id == produto.id,
            Venda.user_id == user_id,
            Venda.data_venda >= inicio,
            Venda.status == 'finalizada'
        ).first()
        
        if not vendas_recentes and produto.estoque_atual > 0:
            # Última venda
            ultima_venda = db.session.query(Venda.data_venda).join(ItemVenda).filter(
                ItemVenda.produto_id == produto.id,
                Venda.user_id == user_id,
                Venda.status == 'finalizada'
            ).order_by(Venda.data_venda.desc()).first()
            
            produtos_parados.append({
                'produto': produto,
                'ultima_venda': ultima_venda[0] if ultima_venda else None,
                'dias_sem_venda': (datetime.now() - ultima_venda[0]).days if ultima_venda else 999
            })
    
    # Ordenar por dias sem venda
    produtos_parados.sort(key=lambda x: x['dias_sem_venda'], reverse=True)
    
    return render_template('relatorios/produtos_parados.html', 
                         produtos_parados=produtos_parados)

# ==================== DASHBOARD EXECUTIVO ====================

# API para KPIs em tempo real
@app.route('/api/dashboard-kpis')
@login_required
def api_dashboard_kpis():
    user_id = session['user_id']
    
    # Período atual vs anterior
    hoje = datetime.now().date()
    inicio_mes_atual = hoje.replace(day=1)
    inicio_mes_anterior = (inicio_mes_atual - timedelta(days=1)).replace(day=1)
    fim_mes_anterior = inicio_mes_atual - timedelta(days=1)
    
    # Vendas do mês atual
    vendas_atual = Venda.query.filter(
        Venda.user_id == user_id,
        Venda.data_venda >= inicio_mes_atual,
        Venda.status == 'finalizada'
    ).all()
    
    # Vendas do mês anterior
    vendas_anterior = Venda.query.filter(
        Venda.user_id == user_id,
        Venda.data_venda.between(inicio_mes_anterior, fim_mes_anterior),
        Venda.status == 'finalizada'
    ).all()
    
    receita_atual = sum(v.valor_total for v in vendas_atual)
    receita_anterior = sum(v.valor_total for v in vendas_anterior)
    
    # Crescimento percentual
    crescimento = ((receita_atual - receita_anterior) / receita_anterior * 100) if receita_anterior > 0 else 0
    
    # Outros KPIs
    total_clientes = Cliente.query.filter_by(user_id=user_id).count()
    produtos_estoque_baixo = Produto.query.filter(
        Produto.user_id == user_id,
        Produto.estoque_atual <= Produto.estoque_minimo
    ).count()
    
    return jsonify({
        'receita_atual': receita_atual,
        'receita_anterior': receita_anterior,
        'crescimento': crescimento,
        'total_clientes': total_clientes,
        'produtos_estoque_baixo': produtos_estoque_baixo,
        'ticket_medio': receita_atual / len(vendas_atual) if vendas_atual else 0
    })

# ==================== SISTEMA DE EXPORTAÇÃO ====================

# Exportação para PDF
@app.route('/relatorios/exportar/<tipo>/<formato>')
@login_required
def exportar_relatorio(tipo, formato):
    user_id = session['user_id']
    
    if formato == 'pdf':
        return exportar_pdf(tipo, user_id)
    elif formato == 'excel':
        return exportar_excel(tipo, user_id)
    elif formato == 'csv':
        return exportar_csv(tipo, user_id)

def exportar_pdf(tipo, user_id):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Título
    title = Paragraph(f"Relatório de {tipo.title()}", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Dados baseados no tipo
    if tipo == 'vendas':
        vendas = Venda.query.filter_by(user_id=user_id).all()
        data = [['Data', 'Cliente', 'Valor', 'Status']]
        for venda in vendas:
            data.append([
                venda.data_venda.strftime('%d/%m/%Y'),
                venda.cliente.nome if venda.cliente else 'N/A',
                f"R$ {venda.valor_total:.2f}",
                venda.status
            ])
    elif tipo == 'produtos':
        produtos = Produto.query.filter_by(user_id=user_id).all()
        data = [['Nome', 'Preço', 'Estoque', 'Categoria']]
        for produto in produtos:
            data.append([
                produto.nome,
                f"R$ {produto.preco:.2f}",
                str(produto.estoque_atual),
                produto.categoria or 'N/A'
            ])
    
    # Criar tabela
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    doc.build(story)
    
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=relatorio_{tipo}.pdf'
    
    return response

def exportar_excel(tipo, user_id):
    buffer = BytesIO()
    
    # Criar workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Relatório {tipo.title()}"
    
    # Estilo do cabeçalho
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    # Dados baseados no tipo
    if tipo == 'vendas':
        vendas = Venda.query.filter_by(user_id=user_id).all()
        headers = ['Data', 'Cliente', 'Valor', 'Status']
        ws.append(headers)
        
        for venda in vendas:
            ws.append([
                venda.data_venda.strftime('%d/%m/%Y'),
                venda.cliente.nome if venda.cliente else 'N/A',
                venda.valor_total,
                venda.status
            ])
    elif tipo == 'produtos':
        produtos = Produto.query.filter_by(user_id=user_id).all()
        headers = ['Nome', 'Preço', 'Estoque', 'Categoria']
        ws.append(headers)
        
        for produto in produtos:
            ws.append([
                produto.nome,
                produto.preco,
                produto.estoque_atual,
                produto.categoria or 'N/A'
            ])
    
    # Aplicar estilo ao cabeçalho
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
    
    # Ajustar largura das colunas
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    wb.save(buffer)
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = f'attachment; filename=relatorio_{tipo}.xlsx'
    
    return response

def exportar_csv(tipo, user_id):
    buffer = BytesIO()
    
    # Dados baseados no tipo
    if tipo == 'vendas':
        vendas = Venda.query.filter_by(user_id=user_id).all()
        data = []
        for venda in vendas:
            data.append({
                'Data': venda.data_venda.strftime('%d/%m/%Y'),
                'Cliente': venda.cliente.nome if venda.cliente else 'N/A',
                'Valor': venda.valor_total,
                'Status': venda.status
            })
    elif tipo == 'produtos':
        produtos = Produto.query.filter_by(user_id=user_id).all()
        data = []
        for produto in produtos:
            data.append({
                'Nome': produto.nome,
                'Preço': produto.preco,
                'Estoque': produto.estoque_atual,
                'Categoria': produto.categoria or 'N/A'
            })
    
    # Converter para DataFrame e depois para CSV
    df = pd.DataFrame(data)
    csv_string = df.to_csv(index=False, encoding='utf-8-sig')
    
    response = make_response(csv_string)
    response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
    response.headers['Content-Disposition'] = f'attachment; filename=relatorio_{tipo}.csv'
    
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
