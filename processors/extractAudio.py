import os
import subprocess
from connectors.celery import celery, current_task
from sqlalchemy.orm import Session
from connectors.database import get_db, ExtractionModel
from functions.createOutputFileName import createOutputFilePath
from functions.s3Functions import generate_s3_object_name, upload_file_to_s3
from datetime import datetime


@celery.task
def extractAudio(
    email: str, video_path: str, codec: str = "mp3", bitrate: str = "192k"
):
    """
    Extract audio from a video file using ffmpeg.
    """
    video_file_name = os.path.splitext(os.path.basename(video_path))[0]
    output_audio_path = createOutputFilePath(video_file_name, "audio")
    command = [
        "ffmpeg",
        "-i",
        video_path,
        "-vn",  # Disable video recording
        "-acodec",
        codec,
        "-b:a",
        bitrate,
        output_audio_path,
    ]
    db: Session = next(get_db())
    # Create a new ExtractionModel instance
    extraction_model = ExtractionModel(
        user_email=email,
        bitrate=bitrate,
        codec=codec,
        task_id=str(current_task.request.id),
    )
    db.add(extraction_model)
    db.commit()
    try:
        subprocess.run(command, check=True)
        print(f"Audio extracted successfully and saved at: {output_audio_path}")

        # Uploading the Data to AWS S3
        s3_object_name = generate_s3_object_name(current_task.request.id)
        upload_file_to_s3(output_audio_path, s3_object_name)
        print("File Upload Complete")
        # Updating Other Model Fields
        extraction_model.end_time = datetime.utcnow()
        extraction_model.status = "Success"
        extraction_model.storage_link = s3_object_name
        db.commit()

        return output_audio_path
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")
        return None
    finally:
        db.close()
