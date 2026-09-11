from fastapi import APIRouter

from services.vector_service import client
from config import COLLECTION_NAME

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


@router.get("/api/documents")
def get_documents():
    """
    Return all unique documents currently stored
    in the AutoMind AI Qdrant knowledge base.
    """

    response = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True,
        with_vectors=False,
    )

    documents = {}

    for point in response[0]:

        payload = point.payload or {}

        filename = payload.get("filename")

        if not filename:
            continue

        if filename not in documents:
            documents[filename] = {
                "filename": filename,
                "chunks": 0,
            }

        documents[filename]["chunks"] += 1

    return {
        "documents": list(documents.values()),
        "total_documents": len(documents),
    }