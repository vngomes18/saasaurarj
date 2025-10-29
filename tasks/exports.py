import time
try:
    from .celery_app import celery, make_celery
except Exception:
    celery = None
    make_celery = None

def export_report_stub(tipo: str, user_id: int, formato: str = 'csv'):
    """Stub síncrono para exportação quando Celery indisponível."""
    time.sleep(1)
    return {
        'status': 'done',
        'tipo': tipo,
        'user_id': user_id,
        'formato': formato,
        'path': f"/static/exports/{tipo}_{user_id}.{formato}"
    }

if celery is not None:
    @celery.task(name='exports.export_report')
    def export_report(tipo: str, user_id: int, formato: str = 'csv'):
        return export_report_stub(tipo, user_id, formato)
else:
    def export_report(tipo: str, user_id: int, formato: str = 'csv'):
        return export_report_stub(tipo, user_id, formato)