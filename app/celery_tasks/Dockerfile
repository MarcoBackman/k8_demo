FROM python:3.9-slim
WORKDIR /app

# Copy requirements and install
COPY ./celery_tasks/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the shared tasks code
COPY . .

# This command tells Celery to look inside the `celery_tasks` package
CMD ["celery", "-A", "celeryapp", "worker", "--loglevel=info"]