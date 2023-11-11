from botocore.exceptions import NoCredentialsError
from connectors.storage import S3, S3_BUCKET_NAME


def upload_file_to_s3(file, object_name):
    try:
        S3.upload_fileobj(file, S3_BUCKET_NAME, object_name)
        return True
    except NoCredentialsError:
        return False


def download_file_from_s3(object_name):
    try:
        response = S3.get_object(Bucket=S3_BUCKET_NAME, Key=object_name)
        return response["Body"].read()
    except NoCredentialsError:
        return None
