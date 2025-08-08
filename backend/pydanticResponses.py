from pydantic import BaseModel
from typing import Dict, Any

class TotalFilesCount(BaseModel):
    total_directories: int
    total_files: int

class AllItems(BaseModel):
    items: list
    description:str
    total: TotalFilesCount