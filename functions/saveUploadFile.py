import os
from fastapi import UploadFile
from BASEDIR import BASE_DIR


def saveUploadFile(file: UploadFile):
    os.makedirs(os.path.join(BASE_DIR, "temp/uploads"), exist_ok=True)
    # Create the file path
    file_path = os.path.join(BASE_DIR, "temp/uploads", file.filename)

    # If the file already exists, delete it
    if os.path.exists(file_path):
        os.remove(file_path)

    # Save the new file
    with open(file_path, "wb") as temp_file:
        temp_file.write(file.file.read())
    print(f"File saved at path: {file_path}")

    return file_path
