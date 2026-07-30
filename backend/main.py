from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AutoMind AI")

# Allow React frontend to access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Welcome to AutoMind AI 🚗",
        "status": "Backend Running Successfully"
    }

@app.get("/api/status")
def get_status():
    return {
        "project": "AutoMind AI",
        "backend": "Running",
        "frontend": "Connected Soon",
        "version": "1.0.0"
    }