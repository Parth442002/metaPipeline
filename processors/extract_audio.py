import subprocess

def extract_audio(input_video_path, output_audio_path, codec='mp3', bitrate='192k'):
    """
    Extract audio from a video file using ffmpeg.
    """
    command = [
        'ffmpeg',
        '-i', input_video_path,
        '-vn',  # Disable video recording
        '-acodec', codec,
        '-b:a', bitrate,
        output_audio_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Audio extracted successfully and saved at: {output_audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")

if __name__=="__main__":
  input_video_path = '../data/yug_ganda_bacha.MP4'
  output_audio_path = '../data/yug_audio.mp3'
  extract_audio(input_video_path, output_audio_path)
