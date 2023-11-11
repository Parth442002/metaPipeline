from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import Response
from dotenv import load_dotenv
import os

load_dotenv()
# Local Imports
from connectors.dbConnector import get_db
from utils.auth import *
from processors.watermark import add_watermark
from functions.saveUploadFile import saveUploadFile

router = APIRouter()

# Security
SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]


@router.post("/")
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


@router.get("/result/{task_id}")
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
