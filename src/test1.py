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
    if process_name != "word_count":
        raise HTTPException(status_code=404, detail="Process not found")
    start_process()
    return {"status": "ok"}


@app.post("/api/{process_name}/stop")
def stop(process_name: str):
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


@app.get("/", response_class=HTMLResponse)
async def read_item():
    return """
    <html>
        <head>
            <title>FastAPI app</title>
        </head>
        <body>
            <h1>Welcome to the FastAPI app</h1>
        </body>
    </html>
    """

static_path = os.path.join(Path(__file__).resolve().parent, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/api/docs", include_in_schema=False)
async def get_documentation():
    return templates.TemplateResponse("documentation.html", {"request": "localhost:8000"})



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
