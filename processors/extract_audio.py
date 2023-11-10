import os
import subprocess
from connectors.celery import celery


@celery.task
def extract_audio(input_video_path, codec="mp3", bitrate="192k"):
    """
    Extract audio from a video file using ffmpeg.
    """
    output_dir = "./temp/output"

    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Extract the video file name from the path
    video_file_name = os.path.splitext(os.path.basename(input_video_path))[0]

    # Generate output_audio_path based on the original video file name
    output_audio_path = os.path.join(
        output_dir, f"{video_file_name}_audio_extracted.mp3"
    )

    command = [
        "ffmpeg",
        "-i",
        input_video_path,
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
