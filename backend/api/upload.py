from fastapi import APIRouter, UploadFile, File
import shutil
import os

from services.pdf_service import extract_text_from_pdf
from services.chunk_service import split_text
from services.embedding_service import generate_embeddings
from services.vector_service import store_embeddings

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pdf_text = extract_text_from_pdf(file_path)

    chunks = split_text(pdf_text)

    embeddings = generate_embeddings(chunks)

    # Store embeddings in Qdrant
    stored = store_embeddings(chunks, embeddings)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "characters": len(pdf_text),
        "chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "vectors_stored": stored,
        "preview": chunks[0] if chunks else ""
    }