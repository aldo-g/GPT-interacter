import httpx
import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from io import BytesIO
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging
import time
import openai
import docx

logging.basicConfig(level=logging.DEBUG)
templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def serve_title_page(request: Request):
    return templates.TemplateResponse("title.html", {"request": request})

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = api_key

def read_docx(file):
    # Convert the temporary file object to a BytesIO object
    file.seek(0)
    bytes_file = BytesIO(file.read())

    doc = docx.Document(bytes_file)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)

async def analyze_cv(cv_text: str) -> str:
    prompt = (
        f"Please provide an in-depth analysis of the following CV, covering at least two chapters. "
        f"Reference specific snippets from the candidate's CV, give special attention to their qualifications and previous experience, "
        f"This is to provide an overview of the candidate to a recruiting company, not an anylsis for a job position. You should however recomend roles that the candidate would be good for"
        f"and provide a rating out of 10 for the candidate:\n\n{cv_text}\n\nIn-depth analysis:"
    )
    
    start_time = time.time()
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    end_time = time.time()
    
    logging.debug(f"Time taken for GPT-3 call: {end_time - start_time} seconds")
    return response.choices[0].text.strip()


class CVAnalysisResponse(BaseModel):
    cv_analysis: str

@app.post("/upload_cv", response_model=CVAnalysisResponse)
async def upload_cv(request: Request, cv: UploadFile = File(...)):
    start_time = time.time()
    cv_text = read_docx(cv.file)
    end_time = time.time()
    
    logging.debug(f"Time taken to read docx: {end_time - start_time} seconds")
    
    start_time = time.time()
    analysis_text = await analyze_cv(cv_text)
    end_time = time.time()
    
    logging.debug(f"Time taken for analyze_cv: {end_time - start_time} seconds")

    return templates.TemplateResponse("analysis.html", {"analysis_text": analysis_text, "request": request})

@app.get("/analyze_cv/")
async def analyze_cv_form(request: Request):
    return templates.TemplateResponse("analyze_cv.html", {"request": request})

@app.get("/static/style/{filename}")
async def get_style(filename: str):
    return FileResponse(f"app/static/style/{filename}")
