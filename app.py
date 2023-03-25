import httpx
import asyncio
from fastapi import FastAPI

app = FastAPI()
openai_api_key = "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"

@app.get("/openai/{text}")
async def get_openai_response(text: str):
    async with httpx.AsyncClient() as client:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }
        data = {
            "prompt": text,
            "max_tokens": 50,
            "temperature": 0.7
        }
        response = await client.post("https://api.openai.com/v1/completions", headers=headers, json=data)
        return response.json()
