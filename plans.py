from functools import wraps
from flask import session, redirect, url_for, flash
from markupsafe import Markup

# Central features per plan
PLAN_FEATURES = {
    'free': {
        'cupons': False,
        'notas_fiscais': False,
        'export_pdf': False,
        'export_excel': False,
        'api_write': False,
        'staff_management': False,
        'reports': False,
    },
    'freepremium': {
        'cupons': True,
        'notas_fiscais': True,
        'export_pdf': True,
        'export_excel': True,
        'api_write': False,
        'staff_management': True,
        'reports': True,
    },
    'premium': {
        'cupons': True,
        'notas_fiscais': True,
        'export_pdf': True,
        'export_excel': True,
        'api_write': True,
        'staff_management': True,
        'reports': True,
    }
}

# Quotas per plan
PLAN_QUOTAS = {
    'free': {
        'produtos_max': 100,
        'clientes_max': 200,
        'vendas_mes_max': 300,
        'nfe_mes_max': 0,
        'cupons_ativos_max': 0,
    },
    'freepremium': {
        'produtos_max': 1000,
        'clientes_max': 2000,
        'vendas_mes_max': 2000,
        'nfe_mes_max': 100,
        'cupons_ativos_max': 10,
    },
    'premium': {
        'produtos_max': None,
        'clientes_max': None,
        'vendas_mes_max': None,
        'nfe_mes_max': None,
        'cupons_ativos_max': None,
    }
}


def get_plan_tier_for_user(user_id: int) -> str:
    """Resolve o plano efetivo para um usuário, preferindo Empresa quando disponível.
    Fallback: UserSettings do admin da mesma empresa."""
    try:
        # Import tardio para evitar ciclos
        from app import User, Empresa, get_user_settings
    except Exception:
        return 'free'

    user = User.query.get(user_id)
    if not user:
        return 'free'

    # Preferir plano por Empresa, se cadastrado
    empresa_record = None
    try:
        empresa_record = Empresa.query.filter_by(nome=user.empresa).first()
    except Exception:
        empresa_record = None

    if empresa_record and empresa_record.plan_tier:
        tier = (empresa_record.plan_tier or 'free').lower()
        return tier if tier in PLAN_FEATURES else 'free'

    # Fallback: usar plano via UserSettings (admin da empresa)
    if user.role == 'admin':
        s = get_user_settings(user_id)
    else:
        admin = User.query.filter_by(empresa=user.empresa, role='admin').first()
        s = get_user_settings(admin.id) if admin else get_user_settings(user_id)
    tier = (s.plan_tier or 'free').lower()
    return tier if tier in PLAN_FEATURES else 'free'


def has_feature(user_id: int, feature: str) -> bool:
    try:
        from app import User
    except Exception:
        return False
    tier = get_plan_tier_for_user(user_id)
    user = User.query.get(user_id)
    # Bloqueio de relatórios para não-admin
    if feature == 'reports' and user and user.role != 'admin':
        return False
    return bool(PLAN_FEATURES.get(tier, {}).get(feature, False))


def require_plan(feature: str):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            uid = session.get('user_id')
            if not uid:
                return redirect(url_for('auth.login'))
            if not has_feature(uid, feature):
                upgrade_link = url_for('planos')
                msg = Markup(
                    f'Recurso indisponível no seu plano. <a href="{upgrade_link}" class="alert-link">Veja os planos</a> para fazer upgrade.'
                )
                flash(msg, 'warning')
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def check_quota_exceeded(user_id: int, quota_key: str, current_count: int) -> bool:
    tier = get_plan_tier_for_user(user_id)
    limit = PLAN_QUOTAS.get(tier, {}).get(quota_key)
    if limit is None:
        return False
    return current_count >= limit