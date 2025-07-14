from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

pending_commands = []

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/submit")
async def submit_command(request: Request):
    data = await request.json()
    pending_commands.append(data["command"])
    return JSONResponse(content={"status": "queued"})

@app.get("/pending")
def get_pending():
    return {"commands": pending_commands}
