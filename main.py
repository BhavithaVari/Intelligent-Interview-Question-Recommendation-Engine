from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import traceback
import shutil
import os
import uuid

from parser import parse_resume, parse_job_description
from gap_analysis import analyze_gaps
from ai_questions import generate_questions

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    temp_path = None

    try:
        print(">>> /analyze endpoint called")

        ext = resume.filename.split(".")[-1]
        temp_path = os.path.join(
            UPLOAD_DIR,
            f"{uuid.uuid4()}.{ext}"
        )

        with open(temp_path, "wb") as f:
            shutil.copyfileobj(resume.file, f)

        resume_data = parse_resume(temp_path)
        jd_data = parse_job_description(job_description)

        gaps = analyze_gaps(
            resume_data["skills"],
            jd_data["required_skills"]
        )

        return {
            "resume_skills": resume_data["skills"],
            "jd_required_skills": jd_data["required_skills"],
            "strengths": gaps["strengths"],
            "gaps": gaps["gaps"],
            "match_percentage": gaps["match_percentage"],
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/generate-questions")
async def generate(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    temp_path = None

    try:
        print(">>> /generate-questions endpoint called")

        ext = resume.filename.split(".")[-1]
        temp_path = os.path.join(
            UPLOAD_DIR,
            f"{uuid.uuid4()}.{ext}"
        )

        with open(temp_path, "wb") as f:
            shutil.copyfileobj(resume.file, f)

        print("Step 1 - Resume Parsing")
        resume_data = parse_resume(temp_path)

        print("Step 2 - JD Parsing")
        jd_data = parse_job_description(job_description)

        print("Step 3 - Gap Analysis")
        gaps = analyze_gaps(
            resume_data["skills"],
            jd_data["required_skills"]
        )

        print("Step 4 - AI Question Generation")

        result = generate_questions(
            strengths=gaps["strengths"],
            gaps=gaps["gaps"],
            jd_text=jd_data["raw_text"],
            resume_text=resume_data["raw_text"],
        )

        print("Step 5 - Success")

        return result

    except Exception as e:
        print("\n========== ERROR ==========")
        traceback.print_exc()
        print("===========================\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)