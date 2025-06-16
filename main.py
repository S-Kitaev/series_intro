from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()

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