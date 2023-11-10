import os
import subprocess
from fastapi import UploadFile
from connectors.celery import celery
from functions.saveUploadFile import saveUploadFile
from functions.createOutputFileName import createOutputFilePath


@celery.task
def extract_audio(video_path: str, codec: str = "mp3", bitrate: str = "192k"):
    """
    Extract audio from a video file using ffmpeg.
    """
    # Extract the video file name from the path
    video_file_name = os.path.splitext(os.path.basename(video_path))[0]
    # Generate output_audio_path based on the original video file name
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

    try:
        subprocess.run(command, check=True)
        print(f"Audio extracted successfully and saved at: {output_audio_path}")
        return output_audio_path
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")
        return None
