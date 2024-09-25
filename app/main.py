from fastapi import FastAPI, __version__, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile, File, HTTPException
from .dtos.ISayHelloDto import ISayHelloDto
from .plan import extract_data
from .routers import system
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)



app = FastAPI()
app.include_router(system.router, prefix="/system")


@app.get("/statuss")
def status():
    return {"ok": True, "version": __version__}


@app.get("/")
def status():
    return {"ok": True, 'page': 'home'}


@app.post("/hello")
async def hello_message(dto: ISayHelloDto):
    return {
        "Filenames": [file.filename for file in dto.files],
    }


@app.get("/api/schedules", response_model=Dict[str, List[Dict[str, Any]]])
async def get_schedules():
    data = extract_data()

    # Group schedules by date
    grouped_schedules = defaultdict(list)

    for schedule in data:
        grouped_schedules[schedule['date']].append(schedule)

    # Sort the grouped schedules by date
    sorted_grouped_schedules = dict(
        sorted(grouped_schedules.items(), key=lambda x: datetime.strptime(x[0], '%d.%m.%Y')))

    return sorted_grouped_schedules


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Upload file to Cloudinary
        response = cloudinary.uploader.upload(file.file)
        return JSONResponse(content={"url": response['url'], "public_id": response['public_id']})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/file/{public_id}")
async def get_file(public_id: str):
    try:
        # Fetch file details from Cloudinary
        response = cloudinary.api.resource(public_id)
        return JSONResponse(content={"url": response['url'], "public_id": response['public_id'], "format": response['format']})
    except cloudinary.exceptions.NotFound:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
