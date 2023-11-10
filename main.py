from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Depends
from fastapi.responses import Response
from connectors.s3Connector import S3_BUCKET_NAME
from functions.s3Functions import upload_file_to_s3, download_file_from_s3
from connectors.celery import celery
from processors.extract_audio import extract_audio
from processors.watermark import add_watermark
from functions.saveUploadFile import saveUploadFile
import os

app = FastAPI()


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
            return Response(
                content=output_audio,
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
            return Response(
                content=output_video,
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
