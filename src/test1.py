import subprocess
import time
import requests
import os
import uvicorn
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi


app = FastAPI()

process = None


import os

def start_process():
    global process
    if process is not None and process.poll() is None:
        raise HTTPException(status_code=400, detail="Process already running")
    path = os.path.abspath(os.path.dirname(__file__))  # получаем абсолютный путь к директории, в которой находится скрипт
    process = subprocess.Popen(["python", os.path.join(path, "word_count.py"), os.path.join(path, "text.txt"), os.path.join(path, "result.txt")], cwd=path)


def stop_process():
    global process
    if process is None:
        raise HTTPException(status_code=404, detail="Process not found")
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        process.kill()
    process = None


def get_process_status():
    global process
    if process is None:
        return {"status": "stopped"}
    if process.poll() is not None:
        process = None
        return {"status": "stopped"}
    return {"status": "running"}


def get_process_result():
    global process
    if process is None:
        raise HTTPException(status_code=404, detail="Process not found")
    if process.poll() is None:
        raise HTTPException(status_code=400, detail="Process is still running")
    path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(path, "result.txt")) as f:
        result = f.read()
    return {"result": result}



@app.post("/api/{process_name}/start")
def start(process_name: str):
    process_name=str(process_name)
    if process_name != "word_count":
        raise HTTPException(status_code=404, detail="Process not found")
    start_process()
    return {"status": "ok"}


@app.post("/api/{process_name}/stop")
def stop(process_name: str):
    process_name=str(process_name)
    if process_name != "word_count":
        raise HTTPException(status_code=404, detail="Process not found")
    stop_process()
    return {"status": "ok"}


@app.get("/api/{process_name}")
def status(process_name: str):
    if process_name != "word_count":
        raise HTTPException(status_code=404, detail="Process not found")
    return get_process_status()


@app.get("/api/{process_name}/result")
def result(process_name: str):
    if process_name != "word_count":
        raise HTTPException(status_code=404, detail="Process not found")
    return get_process_result()


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your Project Name",
        version="1.0.0",
        description="This is a very long description",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@app.get("/api/docs", include_in_schema=False, response_class=HTMLResponse)
async def get_documentation(request: Request):
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="docs",
        oauth2_redirect_url="http://localhost:8000/api/docs/oauth2-redirect",
    )

@app.get("/api/redoc", include_in_schema=False, response_class=HTMLResponse)
async def redoc(request: Request):
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="ReDoc",
        oauth2_redirect_url="http://localhost:8000/api/docs/oauth2-redirect",
    )

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_schema():
    return custom_openapi()

@app.get("/api/docs/oauth2-redirect")
async def oauth2_redirect(request: Request):
    return {"request": request}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
