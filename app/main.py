from fastapi import FastAPI, __version__

from .dtos.ISayHelloDto import ISayHelloDto
from .routers import system

app = FastAPI()
app.include_router(system.router, prefix="/system")

@app.get("/statuss")
def status():
    return {"ok": True, "version": __version__}

@app.post("/hello")
async def hello_message(dto: ISayHelloDto):
    return {
        "Filenames": [file.filename for file in dto.files],
    }