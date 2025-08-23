from celery import Celery
import time
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task
def long_running_task(data: str):
    """5초가 소요되는 무거운 작업을 시뮬레이션합니다."""
    print(f"Celery worker received data: {data}")
    time.sleep(5)
    print("Celery worker finished the task.")
    return f"Successfully processed '{data}'"