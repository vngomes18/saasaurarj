from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from functools import wraps
from config import config

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
    
    # Vendas do mês atual
    inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    vendas_mes = Venda.query.filter(
        Venda.user_id == user_id,
        Venda.data_venda >= inicio_mes,
        Venda.status == 'finalizada'
    ).all()
    
    total_vendas_mes = sum(venda.valor_total for venda in vendas_mes)
    
    # Produtos com estoque baixo
    produtos_estoque_baixo = Produto.query.filter(
        Produto.user_id == user_id,
        Produto.estoque_atual <= Produto.estoque_minimo
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
                         total_vendas_mes=total_vendas_mes,
                         produtos_estoque_baixo=produtos_estoque_baixo,
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
        produto = Produto(
            nome=request.form['nome'],
            descricao=request.form['descricao'],
            preco=float(request.form['preco']),
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
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.preco = float(request.form['preco'])
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
