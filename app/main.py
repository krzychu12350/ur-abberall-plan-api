from fastapi import FastAPI, __version__
from .dtos.ISayHelloDto import ISayHelloDto
from .routers import system
from datetime import datetime
from collections import defaultdict
from datetime import datetime
from time import time

from typing import List, Dict, Any
import openpyxl
import re

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


@app.get("/api/schedules", response_model=[])
async def get_schedules():
    # data = extract_data()
    #
    # # Group schedules by date
    # grouped_schedules = defaultdict(list)
    #
    # for schedule in data:
    #     grouped_schedules[schedule['date']].append(schedule)
    #
    # # Sort the grouped schedules by date
    # sorted_grouped_schedules = dict(
    #     sorted(grouped_schedules.items(), key=lambda x: datetime.strptime(x[0], '%d.%m.%Y')))

    return [1, 2, 3]
