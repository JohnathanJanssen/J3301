import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
import traceback

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

async def ask_jupiter_async(user_message: str) -> str:
    print(f"[DEBUG] ask_jupiter_async received: {user_message}")
    loop = asyncio.get_event_loop()
    try:
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Jupiter."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=300,
                temperature=0.7,
            )
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        tb = traceback.format_exc()
        print(f"[Jupiter Error] {tb}")
        return f"[Jupiter Error] {str(e)}"
