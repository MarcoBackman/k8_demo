from celeryapp import celery_app
import time


@celery_app.task
def long_running_task(data: str):
    """5초가 소요되는 무거운 작업을 시뮬레이션합니다."""
    print(f"Celery worker received data: {data}")
    time.sleep(5)
    print("Celery worker finished the task.")
    return f"Successfully processed '{data}'"
