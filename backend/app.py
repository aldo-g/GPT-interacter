import httpx
import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
import docx
import openai
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from io import BytesIO
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel




app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/", response_class=HTMLResponse)
async def serve_title_page():
    with open("frontend/markup/title.html", "r") as f:
        content = f.read()
    return content

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

def analyze_cv(cv_text: str) -> str:
    prompt = (
        f"Please provide an in-depth analysis of the following CV, covering at least two chapters. "
        f"Reference specific snippets from the candidate's CV, give special attention to their qualifications and previous experience, "
        f"This is to provide an overview of the candidate to a recruiting company, not an anylsis for a job position. You should however recomend roles that the candidate would be good for"
        f"and provide a rating out of 10 for the candidate:\n\n{cv_text}\n\nIn-depth analysis:"
    )    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    analysis_text = response.choices[0].text.strip()
    analysis_text = analysis_text.replace("Quality analysis:", "").strip()

    return analysis_text


class CVAnalysisResponse(BaseModel):
    cv_analysis: str

@app.post("/upload_cv", response_model=CVAnalysisResponse)
async def upload_cv(cv: UploadFile = File(...)):
    cv_text = read_docx(cv.file)
    analysis_text = analyze_cv(cv_text)

    return templates.TemplateResponse("analysis.html", {"request": {"analysis_text": analysis_text}})

@app.get("/analyze_cv/")
async def analyze_cv_form():
    return FileResponse("frontend/markup/analyze_cv.html")

@app.get("/frontend/style/{filename}")
async def get_style(filename: str):
    return FileResponse(f"frontend/style/{filename}")

templates = Jinja2Templates(directory="path/to/your/templates_directory")

