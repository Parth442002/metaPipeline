import subprocess

def add_watermark(input_video_path, watermark_image_path, output_video_path, position='bottom_right'):
    """
    Add a watermark to a video using ffmpeg.
    """
    if isinstance(position, str):
        # Map named positions to coordinates
        position_mapping = {
            'top_left': '10:10',
            'top_right': 'main_w-overlay_w-10:10',
            'bottom_left': '10:main_h-overlay_h-10',
            'bottom_right': 'main_w-overlay_w-10:main_h-overlay_h-10'
        }
        position = position_mapping.get(position.lower())
        if position is None:
            raise ValueError(f"Invalid named position. Choose from: 'top_left', 'top_right', 'bottom_left', 'bottom_right'.")

    command = [
        'ffmpeg',
        '-i', input_video_path,
        '-i', watermark_image_path,
        '-filter_complex', f'overlay={position}',
        output_video_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Watermark added successfully and saved at: {output_video_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error adding watermark: {e}")



if __name__=="__main__":
  input_video_path = '../data/yug_ganda_bacha.MP4'
  watermark_image_path = '../data/watermark.png'
  output_video_path = '../data/yug_watermark.mp4'
  add_watermark(input_video_path, watermark_image_path, output_video_path, position='bottom_right')

