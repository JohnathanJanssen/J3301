from typing import Literal
import re

def orchestrate(user_input: str) -> Literal["fact", "skill", "conversation"]:
    """
    Simple rule-based classifier for now.
    Later, this will use Jupiter's LLM or a local model for smarter routing.
    """

    lowered = user_input.lower().strip()

    if re.search(r"\b(my name is|i am|i live|i was born|my favorite|i like|i prefer|i don’t like)\b", lowered):
        return "fact"
    
    if re.search(r"\b(how do i|can you show me|teach me|what is the best way to)\b", lowered):
        return "skill"

    return "conversation"
from fastapi import FastAPI
from pydantic import BaseModel
import orchestrator

app = FastAPI()

class Message(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Jupiter API is running."}

@app.post("/message")
async def post_message(message: Message):
    try:
        result = orchestrator.orchestrate(message.text)
        return {"message": result}
    except Exception as e:
        return {"message": f"Jupiter encountered an error: {str(e)}"}
