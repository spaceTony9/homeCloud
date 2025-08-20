from datetime import datetime
from fastapi import HTTPException, File, UploadFile
from pathlib import Path
from typing import Optional
import os
import logging
from constants import MAX_FILE_SIZE, ALLOWED_EXTENTIONS
from storage import CloudStorage

class Date:
    @staticmethod
    def convert_date(timestamp):
        d = datetime.fromtimestamp(timestamp)
        formatted_date = d.strftime("%d/%m/%Y, %H:%M:%S")
        return formatted_date
    
def calculate_file_size(size : int):
    if size < 1024:
        return f"{size} B"
    elif size < 1024**2:
        return f"{size // 1024} KB"
    elif size < 1024**3:
        return f"{size // 1024**2} MB"
    else:
        return f"{size // 1024**3} GB"

def validate_filename(filename:str) -> str:
    # Validate name of the file
    if not filename or filename.startswith(".") or "/" in filename:
        raise HTTPException(status_code=400, detail="Invalid Filename")
    # Check if the filename is in allowed extentions
    suffix = Path(filename).suffix.lower()
    if not suffix in ALLOWED_EXTENTIONS:
        raise HTTPException(status_code=400, detail="Unacceptable file extention")
    return filename.lstrip().rstrip()


def find_and_return_file_path(filename: str) -> str:
    validate_filename(filename)
    try:
        for dirpath, dirname, files in os.walk(CloudStorage.send_storage_root()):
            if filename in files:
                file_path = os.path.join(dirpath, filename)
                print(file_path)
                return str(Path(file_path))
    except: 
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found ")
    
def validate_upload_file(file: UploadFile):
    file_extention = Path(file.filename).suffix.lower()
    if not file.filename or file.filename == "":
        print("Hello world")
        raise HTTPException(status_code=404, detail="No file found")
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=412, detail="Exceeding allowed file size")
    if file_extention not in ALLOWED_EXTENTIONS: 
        raise HTTPException(status_code=412, detail="Invalid file extension")