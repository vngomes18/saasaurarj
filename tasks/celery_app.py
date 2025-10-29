try:
    from celery import Celery
except ImportError:
    Celery = None

celery = None

def make_celery(app=None):
    global celery
    if Celery is None:
        print("AVISO: Celery não instalado; usando stubs.")
        return None
    if app is None:
        from app import app as flask_app
        app = flask_app
    celery = Celery(
        app.import_name,
        broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
        backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery