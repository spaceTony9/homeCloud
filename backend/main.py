from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from datetime import datetime
from storage import CloudStorage
from utils import Response
from utils import Date
import shutil
import os

app = FastAPI()  
storage = CloudStorage()

@app.get("/")
async def load_main_page():
    return {"message" : "you are on the main page"}

@app.get("/cloudStorage")
async def show_stored_data():

    
    response = Response().response
    for entry in storage.storage_root.iterdir():
        entry_info = entry.stat()
        date_modified = str(Date.convert_date(entry_info.st_mtime))
        item = {
            "name": entry.name,
            "path": str(entry.relative_to(storage.storage_root)), 
            "type": "directory" if entry.is_dir() else "file", 
            "date_modified" : date_modified
        }

        response["items"].append(item)
        response["total"]["summary"] += 1
        if entry.is_dir():
            response["total"]["summary_directories"] += 1
        else:
            response["total"]["summary_files"] += 1

    return response

@app.post("/upload")
async def upload_file(file: UploadFile = File()):
    file_path = Path.joinpath(storage.storage_root, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"msg": "file created successfully"}

@app.get("/download/{filename}")
async def download_file(filename:str):
    for dirpath, dirname, files in os.walk(storage.storage_root):
        if files == filename:
            print("found")
