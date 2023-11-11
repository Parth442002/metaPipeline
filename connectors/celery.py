from celery import Celery, current_task

celery = Celery(
    __name__,
    broker="redis://redis:6379/0",  # Use the service name from Docker Compose
    backend="redis://redis:6379/0",  # Use the service name from Docker Compose
)
