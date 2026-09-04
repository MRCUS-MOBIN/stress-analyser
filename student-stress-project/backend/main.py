import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.routes import student, assessment, stress, recovery, progress

app = FastAPI(
    title="MindPulse AI - Student Stress & Wellness API",
    description="Backend API for student stress insights, daily check-ins, personalized recovery recommendations, and progress tracking.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(student.router)
app.include_router(assessment.router)
app.include_router(stress.router)
app.include_router(recovery.router)
app.include_router(progress.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Student Stress Detection & Recovery API", "version": "2.0.0"}

# Serve SPA Single Module Index for all legacy HTML endpoints
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
INDEX_FILE = os.path.join(FRONTEND_DIR, "index.html")

@app.get("/{page_name}.html")
def serve_spa_page(page_name: str):
    if os.path.exists(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    return {"message": "Index not found"}

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


