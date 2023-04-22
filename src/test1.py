import subprocess
import time

from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

process = None


def start_process():
    global process
    if process is not None and process.poll() is None:
        raise HTTPException(status_code=400, detail="Process already running")
    process = subprocess.Popen(["python", "word_count.py", "text.txt"])


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
    with open("result.txt") as f:
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


app = FastAPI()

# ...

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

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/api/docs", include_in_schema=False)
async def get_documentation():
    return templates.TemplateResponse("documentation.html", {"request": "localhost:8000"})