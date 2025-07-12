from fastapi import Request
from fastapi.responses import JSONResponse

# Remote message queue (simulate action approvals)
message_queue = []

def queue_message(data: dict):
    message_queue.append(data)
    return {"status": "queued", "queued_length": len(message_queue)}

async def handle_remote_post(req: Request):
    try:
        data = await req.json()
        result = queue_message(data)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
