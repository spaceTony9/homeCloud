from fastapi import FastAPI, UploadFile, File, HTTPException,Response
from fastapi.responses import JSONResponse, PlainTextResponse, FileResponse
from pathlib import Path
from datetime import datetime
from utils import Date, find_and_return_file_path, validate_upload_file
from storage import CloudStorage
from pydanticResponses import TotalFilesCount, AllItems
import shutil
import os

app = FastAPI()  
storage_root_path = CloudStorage.send_storage_root()

@app.get("/")
async def load_main_page():
    return {"message" : "you are on the main page"}

@app.get("/cloudStorage", response_model=AllItems)
async def show_stored_data():
    all_items = []
    total = 0
    total_dir = 0
    total_files = 0
    try:
        if storage_root_path:
            for entry in storage_root_path.iterdir():
                entry_info = entry.stat()
                date_modified = str(Date.convert_date(entry_info.st_mtime))
                item = {
                    "name": entry.name,
                    "path": str(entry.relative_to(storage_root_path)), 
                    "type": "directory" if entry.is_dir() else "file", 
                    "date_modified" : date_modified
                }
                all_items.append(item)
                total += 1
                if entry.is_dir():
                    total_dir += 1
                else:
                    total_files += 1

                total_objects = TotalFilesCount(total_directories=total_dir, total_files=total_files)
    except:
        raise HTTPException(status_code=404, detail="The storage directory was not found")

    return AllItems(items=all_items, description="All stored items", total=total_objects)

@app.post("/uploadFile")
async def upload_file(file: UploadFile):
    validate_upload_file(file)

    # Write check if the already exists
    try:
        file_path = Path.joinpath(storage_root_path, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return JSONResponse(status_code=200, content={
            "message" : "File was successfully uploaded",
            "filename" : file.filename})
    except:
        raise HTTPException(status_code=500, detail="Failed to upload the file")



# @app.get("/download/{filename}")
# async def download_file(filename:str) -> dict:
#     response = response_class.get_response_obj()
#     find_and_return_file_path(filename)
#     response["message"] = "The file is found"
#     return response
