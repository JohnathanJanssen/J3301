import os
import requests
import pygame
import threading
from dotenv import load_dotenv
from datetime import datetime
from uuid import uuid4

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
ELEVEN_VOICE_ID = os.getenv("ELEVEN_VOICE_ID")

AUDIO_OUTPUT_DIR = "audio_output"
audio_lock = threading.Lock()

def synthesize_speech(text: str) -> str:
    if not os.path.exists(AUDIO_OUTPUT_DIR):
        os.makedirs(AUDIO_OUTPUT_DIR)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    unique_id = uuid4().hex[:8]
    filename = f"{timestamp}-{unique_id}.mp3"
    filepath = os.path.join(AUDIO_OUTPUT_DIR, filename)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_API_KEY
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"[ElevenLabs] Saved: {filepath}")
        threading.Thread(target=play_and_cleanup, args=(filepath,), daemon=True).start()
        return filepath
    else:
        print(f"[ElevenLabs] Error {response.status_code}: {response.text}")
        return None

def play_and_cleanup(filepath: str):
    with audio_lock:
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
        except Exception as e:
            print(f"[Audio Playback] Error: {e}")
        finally:
            try:
                os.remove(filepath)
                print(f"[Cleanup] Deleted: {filepath}")
            except Exception as e:
                print(f"[Cleanup] Failed: {e}")
