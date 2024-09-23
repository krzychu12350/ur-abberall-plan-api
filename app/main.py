import uvicorn
from fastapi import FastAPI, __version__
from .routers import system
from plan import extract_data

app = FastAPI()
app.include_router(system.router, prefix="/system")


@app.get("/statuss")
def status():
    return {"ok": True, "version": __version__}


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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
