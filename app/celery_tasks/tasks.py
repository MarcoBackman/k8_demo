# Import the shared Celery app instance
from celery_config import celery_app

@celery_app.task
def long_running_task(data: str):
    """A simple task that simulates work."""
    import time
    print(f"Starting task with data: {data}")
    time.sleep(5)  # Simulate a 5-second task
    print(f"Finished task with data: {data}")
    return f"Processed: {data}"