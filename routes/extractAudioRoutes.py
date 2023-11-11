from fastapi import APIRouter
from fastapi import File, UploadFile, BackgroundTasks
from fastapi.responses import Response
from dotenv import load_dotenv
import os

load_dotenv()
# Local Imports
from utils.auth import *
from processors.extractAudio import extractAudio
from functions.saveUploadFile import saveUploadFile

router = APIRouter()

# Security
SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]


@router.post("/")
async def start_audio_extraction(
    video: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    codec: str = "mp3",
    bitrate: str = "192k",
):
    video_path = saveUploadFile(video)
    # Call the Celery task asynchronously
    task = extractAudio.apply_async(
        args=[video_path], kwargs={"codec": codec, "bitrate": bitrate}
    )
    return {
        "message": f"Audio extraction task started. Task ID: {task.id}",
        "task_Id": task.id,
    }


@router.get("/result/{task_id}")
async def get_task_result(task_id: str):
    task_result = extractAudio.AsyncResult(task_id)
    if task_result.ready():
        if task_result.successful():
            output_audio = task_result.result
            filename = os.path.basename(output_audio)
            with open(output_audio, "rb") as audio_file:
                content = audio_file.read()
            return Response(
                content=content,
                media_type="audio/mp3",
                headers={
                    "Content-Disposition": f"attachment;filename={filename}",
                    "Access-Control-Expose-Headers": "Content-Disposition",
                },
            )
        else:
            return {"message": "Audio extraction failed"}
    else:
        return {"message": "Task is still in progress"}
