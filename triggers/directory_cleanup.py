import os
from datetime import datetime, timedelta
from connectors.celery import celery

"""
# Delete Files which are 30 minutes old
def cleanup_directory(directory: str, threshold_minutes: int):
    current_time = datetime.now()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            age = current_time - creation_time
            if age > timedelta(minutes=threshold_minutes):
                os.remove(file_path)
                print(f"Removed old file: {file_path}")


@celery.task
def cleanup_old_files():
    cleanup_directory("/temp/uploads", 30)
    cleanup_directory("/temp/output", 30)


# Schedule the cleanup task to run every 30 minutes
celery.conf.beat_schedule = {
    "cleanup-task": {
        "task": "cleanup_old_files",
        "schedule": timedelta(minutes=30),
    }
}

"""
