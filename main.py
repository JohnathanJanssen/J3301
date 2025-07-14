from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime
import traceback

from server.llm import ask_jupiter_async
from orchestrator import orchestrate
from server.voice import synthesize_speech

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

LOG_FILE = "jupiter.log"

def log_activity(entry: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{timestamp}] {entry}\n")

class MessageRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Jupiter API is running."}

@app.post("/message")
async def message_endpoint(payload: MessageRequest):
    user_message = payload.text
    try:
        jupiter_reply = await ask_jupiter_async(user_message)
        classification = orchestrate(user_message)
        print(f"[Orchestrator] Classified as: {classification}")

        audio_file = synthesize_speech(jupiter_reply)

        log_entry = (
            f'UserInput="{user_message}" '
            f'Classification="{classification}" '
            f'JupiterReply="{jupiter_reply}"'
        )
        log_activity(log_entry)

        return {
            "message": jupiter_reply,
            "classification": classification,
            "audio_file": audio_file
        }
    except Exception as e:
        tb = traceback.format_exc()
        print(f"[Jupiter Error] {tb}")
        log_activity(f"Exception occurred: {str(e)}")
        return {"message": f"Jupiter encountered an error: {str(e)}"}
