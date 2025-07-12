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
