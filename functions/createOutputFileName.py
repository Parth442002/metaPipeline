import os


def createOutputFilePath(file_name: str, type: str = "audio"):
    """
    Create the output file path based on the specified operation.
    """
    os.makedirs("./temp/output", exist_ok=True)
    fileType = {"audio": "extracted_audio", "video": "watermarked_video"}
    file_extension = ".mp3" if type == "audio" else ".mp4"
    output_file_name = f"{file_name}_{fileType[type]}{file_extension}"
    if os.path.exists(f"./temp/output/{output_file_name}"):
        os.remove(f"./temp/output/{output_file_name}")

    return os.path.join("./temp/output", output_file_name)
