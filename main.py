from fastapi import FastAPI, __version__
import cloudinary.api
from plan import extract_data
from typing import List, Dict, Any
from collections import defaultdict
from datetime import datetime
from time import time

# Configure Cloudinary
cloudinary.config(
    cloud_name="dysdefjin",
    api_key="388545225291945",
    api_secret="ZMVVwenZXy4sYR6qdUo-k5w23hY"
)

app = FastAPI()


@app.get("/api/json")
async def ping():
    return {"message": "pong"}


@app.get("/api/plan")
async def ping():
    data = extract_data()
    # print(data)
    return {"data": data}


@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}


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
