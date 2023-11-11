import subprocess
from connectors.celery import celery
from functions.createOutputFileName import createOutputFilePath
import os


@celery.task
def addWatermark(video_path: str, watermark_path: str, position="bottom_right"):
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

    try:
        subprocess.run(command, check=True)
        print(f"Watermark added successfully and saved at: {output_video_path}")
        return output_video_path
    except subprocess.CalledProcessError as e:
        print(f"Error adding watermark: {e}")
