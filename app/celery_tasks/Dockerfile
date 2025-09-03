FROM python:3.9-slim
WORKDIR /app

# Install dependencies
COPY ./app/celery_tasks/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- CORRECTED COPY COMMANDS ---
# Copy the celery_tasks directory to /app/celery_tasks
COPY ./app/celery_tasks ./celery_tasks

# Copy the config file to the root of the workdir /app
COPY ./app/celery_config.py .

# Command to start the Celery worker
CMD ["celery", "-A", "celery_config.celery_app", "worker", "--loglevel=info"]