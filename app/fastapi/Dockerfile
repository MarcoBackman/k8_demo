FROM python:3.9-slim
WORKDIR /app

# Copy requirements and install
COPY ./fastapi/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code AND the shared tasks code
COPY ./fastapi/app.py .
COPY ./celery_tasks ./celery_tasks

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]