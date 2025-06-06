import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import openai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    prompt: str


def sanitize(message: str) -> str:
    key = openai.api_key
    if key:
        message = message.replace(key, "[REDACTED]")
    return message

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        resp = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": req.prompt}],
        )
        return {"response": resp.choices[0].message.content}
    except openai.OpenAIError as exc:
        status = getattr(exc, "status_code", 500)
        msg = sanitize(str(exc))
        logger.error("OpenAI API error", extra={"openai_status": status, "error": msg}, exc_info=exc)
        return JSONResponse(status_code=status, content={"error": msg})
    except Exception as exc:
        logger.exception("Unhandled server error")
        raise HTTPException(status_code=500, detail={"error": "Internal server error"})
