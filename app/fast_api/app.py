from fastapi import FastAPI
from celery_tasks.tasks import celery_app, long_running_task

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running."}

@app.post("/start-task")
def start_task():
    """Celery 작업을 시작시키는 API 엔드포인트"""
    task = long_running_task.delay("This is a heavy task!")
    return {"message": "Task has been sent to the Celery worker.", "task_id": task.id}