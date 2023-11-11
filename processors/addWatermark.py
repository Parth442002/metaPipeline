import os
import subprocess
from connectors.celery import celery, current_task
from sqlalchemy.orm import Session
from connectors.database import get_db, WatermarkModel
from functions.createOutputFileName import createOutputFilePath
from functions.s3Functions import generate_s3_object_name, upload_file_to_s3
from datetime import datetime


@celery.task
def addWatermark(
    email: str, video_path: str, watermark_path: str, position="bottom_right"
):
    video_file_name = os.path.splitext(os.path.basename(video_path))[0]
    output_video_path = createOutputFilePath(video_file_name, "video")
    if isinstance(position, str):
        # Map named positions to coordinates
        position_mapping = {
            "top_left": "10:10",
            "top_right": "main_w-overlay_w-10:10",
            "bottom_left": "10:main_h-overlay_h-10",
            "bottom_right": "main_w-overlay_w-10:main_h-overlay_h-10",
        }
        position = position_mapping.get(position.lower())
        if position is None:
            raise ValueError(
                f"Invalid named position. Choose from: 'top_left', 'top_right', 'bottom_left', 'bottom_right'."
            )
    command = [
        "ffmpeg",
        "-i",
        video_path,
        "-i",
        watermark_path,
        "-filter_complex",
        f"overlay={position}",
        output_video_path,
    ]
    db: Session = next(get_db())
    # Create a new ExtractionModel instance
    extraction_model = WatermarkModel(
        user_email=email,
        video_path=video_path,
        watermark_path=watermark_path,
        position=position,
        task_id=str(current_task.request.id),
    )
    db.add(extraction_model)
    db.commit()
    try:
        subprocess.run(command, check=True)
        print(f"Watermark added successfully and saved at: {output_video_path}")

        s3_object_name = generate_s3_object_name(
            current_task.request.id, file_type="video_files"
        )
        upload_file_to_s3(output_video_path, s3_object_name)
        print("File Upload Complete")

        # Updating Other Model Fields
        extraction_model.end_time = datetime.utcnow()
        extraction_model.status = "Success"
        extraction_model.storage_link = s3_object_name
        extraction_model.local_link = output_video_path
        db.commit()

        return output_video_path
    except subprocess.CalledProcessError as e:
        print(f"Error adding watermark: {e}")
    finally:
        db.close()
