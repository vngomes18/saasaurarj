import time
try:
    from .celery_app import celery
except Exception:
    celery = None

def send_reset_password_stub(email: str, temp_password: str):
    time.sleep(0.5)
    return {'status': 'sent', 'email': email}

if celery is not None:
    @celery.task(name='emails.send_reset_password')
    def send_reset_password(email: str, temp_password: str):
        return send_reset_password_stub(email, temp_password)
else:
    def send_reset_password(email: str, temp_password: str):
        return send_reset_password_stub(email, temp_password)