from botocore.exceptions import NoCredentialsError
from connectors.storage import S3, S3_BUCKET_NAME


def generate_s3_object_name(task_id: str, file_type: str = "audio_files"):
    if file_type == "audio_files":
        return f"{file_type}/{task_id}.mp3"
    elif file_type == "video_files":
        return f"{file_type}/{task_id}.mp4"


def upload_file_to_s3(file_path: str, object_name: str):
    S3.upload_file(file_path, S3_BUCKET_NAME, object_name)


def download_file_from_s3(object_name):
    try:
        response = S3.get_object(Bucket=S3_BUCKET_NAME, Key=object_name)
        return response["Body"].read()
    except NoCredentialsError:
        return None
