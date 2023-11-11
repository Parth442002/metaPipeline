from fastapi import APIRouter
from fastapi import File, UploadFile, BackgroundTasks
from fastapi.responses import Response
from dotenv import load_dotenv
import os

load_dotenv()
# Local Imports
from utils.auth import *
from processors.addWatermark import addWatermark
from functions.saveUploadFile import saveUploadFile
from connectors.database import WatermarkModel, get_db

router = APIRouter()


@router.get("/")
async def allWatermarks(
    email: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        # Fetch ExtractionModels related to the current user
        watermark_models = db.query(WatermarkModel).filter_by(user_email=email).all()
        return watermark_models
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db.close()


@router.post("/")
async def waterMarkingRoute(
    email: str = Depends(get_current_user),
    video: UploadFile = File(...),
    watermark: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    position: str = "bottom_right",
):
    video_path = saveUploadFile(video)
    watermark_path = saveUploadFile(watermark)
    # Call the Celery task asynchronously
    task = addWatermark.apply_async(
        args=[
            email,
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
async def resultRoute(task_id: str):
    task_result = addWatermark.AsyncResult(task_id)
    if task_result.ready():
        if task_result.successful():
            output_video = task_result.result
            import pdb

            pdb.set_trace()
            if output_video and os.path.exists(output_video):
                filename = os.path.basename(output_video)
                with open(output_video, "rb") as audio_file:
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
                return {"message": "Audio extraction failed or file not found"}
        else:
            return {"message": "Audio extraction task failed"}
    else:
        return {"message": "Task is still in progress"}
