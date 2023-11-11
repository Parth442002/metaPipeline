from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import Response
import os
from connectors.celery import celery
from dotenv import load_dotenv
import os

load_dotenv()

# Local Imports
from processors.extract_audio import extract_audio
from processors.watermark import add_watermark
from functions.saveUploadFile import saveUploadFile
from routes.userAuthRoutes import router as userAuthRouter
from routes.extractAudioRoutes import router as audioRouter
from routes.watermarkRoutes import router as watermarkRouter

app = FastAPI()

# ? Auth Routes
app.include_router(userAuthRouter, prefix="/auth", tags=["auth"])
app.include_router(audioRouter, prefix="/audio", tags=["audio"])
app.include_router(watermarkRouter, prefix="/watermark", tags=["watermark"])


"""
@app.post("/extract-audio/")
async def start_audio_extraction(
    video: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    codec: str = "mp3",
    bitrate: str = "192k",
):
    video_path = saveUploadFile(video)
    # Call the Celery task asynchronously
    task = extract_audio.apply_async(
        args=[video_path], kwargs={"codec": codec, "bitrate": bitrate}
    )
    return {
        "message": f"Audio extraction task started. Task ID: {task.id}",
        "task_Id": task.id,
    }


@app.get("/audio-result/{task_id}")
async def get_task_result(task_id: str):
    task_result = extract_audio.AsyncResult(task_id)
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


# Routes for adding watermarks
@app.post("/add-watermark/")
async def start_watermarking(
    video: UploadFile = File(...),
    watermark: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    position: str = "bottom_right",
):
    video_path = saveUploadFile(video)
    watermark_path = saveUploadFile(watermark)

    # Call the Celery task asynchronously
    task = add_watermark.apply_async(
        args=[
            video_path,
            watermark_path,
        ],
        kwargs={"position": position},
    )
    return {
        "message": f"Watermark Application task started. Task ID: {task.id}",
        "task_Id": task.id,
    }


@app.get("/watermark-result/{task_id}")
async def get_watermarked_result(task_id: str):
    task_result = add_watermark.AsyncResult(task_id)
    if task_result.ready():
        if task_result.successful():
            output_video = task_result.result
            filename = os.path.basename(output_video)
            with open(output_video, "rb") as video_file:
                content = video_file.read()
            return Response(
                content=content,
                media_type="video/mp4",
                headers={
                    "Content-Disposition": f"attachment;filename={filename}",
                    "Access-Control-Expose-Headers": "Content-Disposition",
                },
            )
        else:
            return {"message": "Watermarking failed"}
    else:
        return {"message": "Task is still in progress"}

"""
