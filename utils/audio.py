# utils/audio.py

import pygame
import time

def play_audio(path):
    try:
        pygame.mixer.quit()  # Force reinit to avoid stuck states
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"[AUDIO ERROR] {e}")
