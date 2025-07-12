from fastapi import FastAPI, Request
from pydantic import BaseModel
import pyttsx3
import platform
import webbrowser
import subprocess
import random
import datetime

app = FastAPI()
voice = pyttsx3.init()

# --- Models ---
class RemoteCommand(BaseModel):
    action: str
    payload: dict = {}

# --- Voice Utility ---
def say(text):
    variants = [
        f"{text}",
        f"Spoken: {text}.",
        f"As you said: {text}.",
        f"I have spoken: {text}.",
        f"Message received: {text}.",
        f"Repeating back: {text}.",
        f"Understood. {text}.",
        f"Acknowledged. {text}.",
        f"{text}, Architect."
    ]
    voice.say(random.choice(variants))
    voice.runAndWait()

# --- Command Handler ---
def handle_remote_command(data: RemoteCommand):
    action = data.action.lower()
    payload = data.payload

    if action == "say":
        text = payload.get("text", "No message provided.")
        say(text)
        return {"status": "ok", "message": f"Spoken: {text}"}

    elif action == "respond":
        text = payload.get("text", "No response configured.")
        return {"status": "ok", "message": text}

    elif action == "system_info":
        info = {
            "os": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return {"status": "ok", "system": info}

    elif action == "open_browser":
        url = payload.get("url", "https://www.google.com")
        webbrowser.open(url)
        return {"status": "ok", "message": f"Pretending to open {url}"}

    elif action == "run_script":
        script_path = payload.get("path")
        if not script_path:
            return {"status": "error", "message": "No script path provided."}
        try:
            subprocess.Popen(script_path, shell=True)
            return {"status": "ok", "message": f"Script triggered: {script_path}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif action == "log":
        message = payload.get("text", "No message")
        with open("jupiter_log.txt", "a") as log:
            log.write(f"[{datetime.datetime.now()}] {message}\n")
        return {"status": "ok", "message": "Logged to file."}

    return {"status": "error", "message": f"Unknown action: {action}"}

# --- Routes ---
@app.get("/")
async def root():
    return {"status": "Jupiter is online"}

@app.post("/jupiter/remote")
async def remote_entry(request: Request):
    try:
        json_data = await request.json()
        cmd = RemoteCommand(**json_data)
        result = handle_remote_command(cmd)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}