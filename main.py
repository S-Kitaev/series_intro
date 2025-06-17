import os
import shutil

from fastapi import Request, FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse

from backend.detector import IntroDetector

app = FastAPI()

# инициализация детектора
MODEL_PATH = "backend/models/model.pt"
detector = IntroDetector(MODEL_PATH)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/images", StaticFiles(directory="frontend/images"), name="images")

templates = Jinja2Templates(directory="frontend")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("frontend/images/logo.png")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Возвращаем шаблон home.html без динамического контекста
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/detect_intro/")
async def detect_intro(file: UploadFile = File(...)):
    # сохраняем временно
    tmp_path = f"/tmp/{file.filename}"
    with open(tmp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        start, end = detector.detect(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # убираем временный файл
    os.remove(tmp_path)

    if start is None:
        return JSONResponse({"message": "Intro not found"}, status_code=404)

    return {"start": start, "end": end}