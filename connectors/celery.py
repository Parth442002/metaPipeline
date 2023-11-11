from celery import Celery, current_task

celery = Celery(
    __name__,
    broker="redis://redis:6379/0",  # DEPLOYMENT
    backend="redis://redis:6379/0",  # Deployment
    # broker="redis://127.0.0.1:6379/0",
    # backend="redis://127.0.0.1:6379/0",
)
