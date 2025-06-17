import os
import shutil
import traceback

from fastapi import Request, FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse

from backend.detector import detect_intro

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/images", StaticFiles(directory="frontend/images"), name="images")

templates = Jinja2Templates(directory="frontend")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("frontend/images/logo.png")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/detect_intro/")
async def detect_intro_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    # будем работать ос временным файлом
    tmp = f"temp_{file.filename}"
    with open(tmp, "wb") as out:
        shutil.copyfileobj(file.file, out)

    background_tasks.add_task(os.remove, tmp)
    await file.close()

    # Детектирование
    try:
        start, end = detect_intro(tmp)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

    if start is None:
        return JSONResponse({"message": "Intro not found"}, status_code=404)

    return {"start": start, "end": end}