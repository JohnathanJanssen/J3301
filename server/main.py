from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from llm import ask_jupiter_async
from orchestrator import orchestrate
import pygame
import threading
from dotenv import load_dotenv

# === Load environment ===
load_dotenv()
app = FastAPI()

# === Enable CORS (optional for web GUI access) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# === Request schema ===
class MessageRequest(BaseModel):
    text: str

# === Wake-up audio ===
def play_jupiter_wake_up():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("audio_output/jupiter_wake_up.mp3")
        pygame.mixer.music.play()
    except Exception as e:
        print(f"[Startup Audio] Failed to play Jupiter's boot voice: {e}")

threading.Thread(target=play_jupiter_wake_up, daemon=True).start()

# === Main message route ===
@app.post("/message")
async def message_endpoint(payload: MessageRequest):
    user_message = payload.text
    try:
        jupiter_reply = await ask_jupiter_async(user_message)

        # Route memory classification
        orchestrate(user_message, jupiter_reply)

        return {"message": jupiter_reply}
    except Exception as e:
        return {"message": f"Jupiter encountered an error: {str(e)}"}
