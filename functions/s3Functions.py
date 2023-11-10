from botocore.exceptions import NoCredentialsError
from connectors.s3Connector import S3, S3_BUCKET_NAME


def upload_file_to_s3(file, bucket_name, object_name):
    try:
        S3.upload_fileobj(file, bucket_name, object_name)
        return True
    except NoCredentialsError:
        return False


def download_file_from_s3(bucket_name, object_name):
    try:
        response = S3.get_object(Bucket=bucket_name, Key=object_name)
        return response["Body"].read()
    except NoCredentialsError:
        return None
