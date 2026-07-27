from fastapi import FastAPI

app = FastAPI(
    title="AutoMind AI",
    description="A Multi-Agent Generative AI Workspace for Automotive Engineering",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to AutoMind AI 🚗",
        "status": "Backend Running Successfully"
    }