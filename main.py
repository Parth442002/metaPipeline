from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse,Response
from botocore.exceptions import NoCredentialsError
from connectors.s3Connector import S3,S3_BUCKET_NAME
import io
app = FastAPI()


def upload_file_to_s3(file, bucket_name, object_name):
    try:
        S3.upload_fileobj(file, bucket_name, object_name)
        return True
    except NoCredentialsError:
        return False

def download_file_from_s3(bucket_name, object_name):
    try:
        response = S3.get_object(Bucket=bucket_name, Key=object_name)
        return response['Body'].read()
    except NoCredentialsError:
        return None

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    object_name = f"uploads/{file.filename}"
    if upload_file_to_s3(file.file, S3_BUCKET_NAME, object_name):
        return {"message": "File uploaded successfully"}
    else:
        return {"message": "Failed to upload file"}

@app.get("/download-file/")
async def download_file(filename: str):
    object_name = f"uploads/{filename}"
    file_content = download_file_from_s3(S3_BUCKET_NAME, object_name)
    if file_content is not None:
        #Attachment->Download
        #inline-> Display file
        return Response(
            content=file_content,
            headers={
                "Content-Disposition":f"inline;filename={filename}",
                'Content-type':"application/octet-stream",
                'Access-Control-Expose-Headers':"Content-Disposition",
            }
        )
    else:
        return {"message": "File not found"}

