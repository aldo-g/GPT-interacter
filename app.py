import httpx
import asyncio
from fastapi import FastAPI
import openai
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

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

def ping_openai_api():
    try:
        models = openai.Model.list()
        return True
    except Exception as e:
        return False