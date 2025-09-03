from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://redis-service:6379/0',
    backend='redis://redis-service:6379/0',
    # This tells the worker to look for tasks inside 'celery_tasks/tasks.py'
    include=['celery_tasks.tasks']
)

celery_app.conf.update(
    task_track_started=True,
)