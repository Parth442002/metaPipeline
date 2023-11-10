from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from connectors.s3Connector import S3_BUCKET_NAME
from functions.s3Functions import upload_file_to_s3, download_file_from_s3

app = FastAPI()


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
        # Attachment->Download
        # inline-> Display file
        return Response(
            content=file_content,
            headers={
                "Content-Disposition": f"inline;filename={filename}",
                "Content-type": "application/octet-stream",
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )
    else:
        return {"message": "File not found"}
