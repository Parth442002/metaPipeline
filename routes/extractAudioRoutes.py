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
from connectors.database import get_db, ExtractionModel, UserModel

router = APIRouter()


# ? All User Audio Extractions
@router.get("/")
async def get_user_extraction_models(
    email: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        # Fetch ExtractionModels related to the current user
        extraction_models = db.query(ExtractionModel).filter_by(user_email=email).all()
        return extraction_models
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db.close()


# ? Individual User Audio Extraction
@router.get("/{extraction_id}")
async def get_single_extraction(
    extraction_id: int,
    email: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        extraction = (
            db.query(ExtractionModel)
            .filter_by(id=extraction_id, user_email=email)
            .first()
        )
        if extraction is None:
            raise HTTPException(status_code=404, detail="Extraction not found")
        return extraction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db.close()


@router.post("/")
async def extractAudioRoute(
    email: str = Depends(get_current_user),
    video: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    codec: str = "mp3",
    bitrate: str = "192k",
):
    video_path = saveUploadFile(video)
    print(video_path)
    # Call the Celery task asynchronously
    task = extractAudio.apply_async(
        args=[email, video_path], kwargs={"codec": codec, "bitrate": bitrate}
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
            if output_audio and os.path.exists(output_audio):
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
                return {"message": "Audio extraction failed or file not found"}
        else:
            return {"message": "Audio extraction task failed"}
    else:
        return {"message": "Task is still in progress"}
