FROM python:3.9-slim
WORKDIR /app

# The path to requirements.txt has changed
COPY ./app/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code using the new folder name
COPY ./app/api ./api
COPY ./app/celery_tasks ./celery_tasks
COPY ./app/celery_config.py .

# The command to run the server also uses the new name
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]