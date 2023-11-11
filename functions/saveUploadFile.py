import os
from fastapi import UploadFile


def saveUploadFile(file: UploadFile):
    import pdb

    os.makedirs("./temp/uploads", exist_ok=True)
    # Create the file path
    file_path = os.path.join("./temp/uploads", file.filename)
    # If the file already exists, delete it
    if os.path.exists(file_path):
        os.remove(file_path)

    # Save the new file
    with open(file_path, "wb") as temp_file:
        temp_file.write(file.file.read())

    return file_path