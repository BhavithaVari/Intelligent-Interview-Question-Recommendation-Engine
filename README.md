# Intelligent-Interview-Question-Recommendation-Engine
## Overview

The Intelligent Interview Question Recommendation Engine is an AI-powered application that analyzes a candidate's resume and a job description to generate structured interview questions.

The application extracts skills from the resume, compares them with the required skills from the job description, identifies strengths and missing skills, and uses AI to generate interview questions with evaluation criteria.

## Features

- Upload Resume (PDF or DOCX)
- Enter Job Description
- Extract technical skills from the resume
- Compare resume skills with job requirements
- Identify candidate strengths
- Identify missing or unclear skills
- Generate AI-powered interview questions
- Assign difficulty levels (Easy, Medium, Hard)
- Provide expected answer points
- Explain why each question was selected
- Approve or reject generated interview questions
- REST API built with FastAPI
- Interactive user interface built with Streamlit

---

## Technologies Used

### Frontend
- Streamlit

### Backend
- FastAPI
- Python

### AI
- Groq Llama 3.3 70B Versatile

### Python Libraries
- pdfplumber
- python-docx
- groq
- python-dotenv
- requests
- uvicorn
- python-multipart

---

## Project Structure

```
Assignment 2/
│
├── backend/
│   ├── ai_questions.py
│   ├── gap_analysis.py
│   ├── main.py
│   ├── parser.py
│   ├── test.py
│   ├── .env
│   ├── uploads/
│   └── venv/
│
├── app.py
└── venv/
```

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

### 4. Start the FastAPI backend

Navigate to the backend folder and run:

```bash
uvicorn main:app --reload
```

The backend will run at:

```
http://127.0.0.1:8000
```

API documentation:

```
http://127.0.0.1:8000/docs
```

### 5. Start the Streamlit application

From the project directory, run:

```bash
streamlit run app.py
```

---

## Application Workflow

1. Upload a candidate's resume (PDF or DOCX).
2. Paste the job description.
3. Resume text is extracted.
4. Skills are identified from the resume.
5. Required skills are extracted from the job description.
6. Resume skills are compared with job requirements.
7. Candidate strengths and missing skills are identified.
8. AI generates interview questions based on:
   - Required technical skills
   - Candidate strengths
   - Missing or weak skills
   - Practical problem-solving scenarios
9. Generated questions include:
   - Difficulty level
   - Expected answer points
   - Reason for selection
10. The interviewer can approve or reject questions.

---

## API Endpoints

### Health Check

```
GET /health
```

Returns:

```json
{
  "status": "ok"
}
```

### Analyze Resume

```
POST /analyze
```

Returns:

- Resume skills
- Required skills
- Candidate strengths
- Missing skills
- Match percentage

### Generate Interview Questions

```
POST /generate-questions
```

Returns AI-generated interview questions with:

- Question
- Difficulty
- Expected answer points
- Reason for selection

---

## Assumptions

- Resumes are provided in PDF or DOCX format.
- Job descriptions are entered as plain text.
- Skill extraction is based on a predefined technical skill vocabulary.
- AI returns valid structured JSON responses.
- Uploaded files are stored temporarily for processing.

---

## Trade-offs

- Skill extraction uses keyword matching rather than semantic embeddings.
- Uploaded files are stored locally and deleted after processing.
- Question approval/rejection is maintained only during the current session.
- No database is used to persist interview history.

---

## AI Tools Used

### ChatGPT

Used for:
- Project planning
- Backend architecture guidance
- FastAPI implementation assistance
- Streamlit UI guidance
- Prompt engineering
- Debugging support
- Documentation preparation

### Groq Llama 3.3 70B Versatile

Used for:
- Generating interview questions
- Assigning difficulty levels
- Generating expected answer points
- Explaining why each question was selected

---

## Testing

Basic testing was performed to verify:

- Resume parsing
- Skill extraction
- Skill gap analysis
- API endpoint functionality
- AI response generation

---

## Future Improvements

- Edit generated interview questions
- Store interview history in a database
- Export interview plans as PDF or JSON
- Semantic skill matching using embeddings
- User authentication and role management
- Deploy the application to a cloud platform

---

## Author
Bhavitha Vari
Developed as part of the Intelligent Interview Question Recommendation Engine assignment.
