import asyncio

async def ask_jupiter_async(user_message: str) -> str:
    # Placeholder logic: echo the user's message with a prefix
    await asyncio.sleep(0.1)  # Simulate async processing
    return f"Jupiter received: {user_message}"