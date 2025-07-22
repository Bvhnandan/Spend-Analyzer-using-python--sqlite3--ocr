import os
from uuid import uuid4

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_uploaded_file(upload_file):
    file_ext = upload_file.filename.split('.')[-1]
    fname = f"{uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_FOLDER, fname)

    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())
    return file_path
