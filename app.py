import httpx
import asyncio
from fastapi import FastAPI
import openai
import os
from dotenv import load_dotenv
from doc_extractor import cv_text

app = FastAPI()

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

def analyze_cv(cv_text):
    prompt = f"Please analyze the quality of the following CV:\n\n{cv_text}\n\nQuality analysis:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

analysis = analyze_cv(cv_text)
print("CV Analysis:", analysis)