from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://redis-service:6379/0',
    backend='redis://redis-service:6379/0'
)

celery_app.conf.update(
    task_track_started=True,
)