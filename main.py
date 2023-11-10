from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Depends
from fastapi.responses import Response
from connectors.s3Connector import S3_BUCKET_NAME
from functions.s3Functions import upload_file_to_s3, download_file_from_s3
from connectors.celery import celery
from processors.extract_audio import extract_audio
import os

app = FastAPI()


@app.post("/extract-audio/")
async def start_audio_extraction(
    input_video_file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    codec: str = "mp3",
    bitrate: str = "192k",
):
    upload_dir = "./temp/uploads"

    # Ensure the directory exists
    os.makedirs(upload_dir, exist_ok=True)
    # Save the uploaded video file to a temporary location
    temp_video_path = f"./temp/uploads/{input_video_file.filename}"
    with open(temp_video_path, "wb") as temp_video:
        temp_video.write(input_video_file.file.read())

    # Call the Celery task asynchronously
    task = extract_audio.apply_async(
        args=[temp_video_path], kwargs={"codec": codec, "bitrate": bitrate}
    )

    return {"message": f"Audio extraction task started. Task ID: {task.id}"}


@app.get("/audio-result/{task_id}")
async def get_task_result(task_id: str):
    task_result = extract_audio.AsyncResult(task_id)
    if task_result.ready():
        if task_result.successful():
            # Task succeeded, return the extracted audio file
            return Response(
                content=task_result.result,
                media_type="audio/mp3",
                headers={
                    "Content-Disposition": f"attachment;filename=audio_result.mp3",
                    "Access-Control-Expose-Headers": "Content-Disposition",
                },
            )
        else:
            return {"message": "Audio extraction failed"}
    else:
        return {"message": "Task is still in progress"}
