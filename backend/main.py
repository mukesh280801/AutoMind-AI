from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.status import router as status_router
from api.upload import router as upload_router
from api.chat import router as chat_router


app = FastAPI(
    title="AutoMind AI"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Routers
# =========================================================

app.include_router(status_router)
app.include_router(upload_router)
app.include_router(chat_router)