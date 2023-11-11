from celery import Celery, current_task
import os
from dotenv import load_dotenv

load_dotenv()
celery = Celery(
    __name__,
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)
