from typing import List

from fastapi import UploadFile, File
from pydantic import BaseModel

class ISayHelloDto(BaseModel):
    files: List[UploadFile]