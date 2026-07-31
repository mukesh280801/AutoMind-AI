from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Welcome to AutoMind AI 🚗",
        "status": "Backend Running Successfully"
    }


@router.get("/api/status")
def get_status():
    return {
        "project": "AutoMind AI",
        "backend": "Running",
        "frontend": "Connected",
        "version": "1.0.0"
    }