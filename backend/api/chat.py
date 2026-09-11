from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from services.chat_orchestrator import process_chat
from services.llm_service import generate_answer_stream
from services.memory_service import (
    get_history,
    add_message
)
from services.intent_service import detect_intent
from services.retrieval_service import get_top_k
from services.query_rewrite_service import rewrite_question
from services.search_service import search_documents
from services.compression_service import compress_context

from services.logging_service import get_logger


router = APIRouter()

logger = get_logger("chat_api")


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)


# =========================================================
# Normal Chat
# =========================================================

@router.post("/api/chat")
async def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    logger.info(
        "Chat request received: %s",
        question
    )

    try:

        response = process_chat(question)

        logger.info(
            "Chat request completed successfully"
        )

        return response

    except Exception as e:

        logger.exception(
            "Chat request failed: %s",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail="AutoMind AI failed to process the question."
        )


# =========================================================
# Streaming Chat
# =========================================================

@router.post("/api/chat/stream")
async def stream_chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    logger.info(
        "Streaming chat request received: %s",
        question
    )

    try:

        intent = detect_intent(question)

        logger.info(
            "Streaming intent detected: %s",
            intent
        )

        # -------------------------------------------------
        # Greeting / Small Talk
        # -------------------------------------------------

        if intent == "greeting":

            def greeting_stream():

                yield (
                    "Hello! 👋 I am AutoMind AI. "
                    "How can I help you today?"
                )

            return StreamingResponse(
                greeting_stream(),
                media_type="text/plain"
            )

        if intent == "smalltalk":

            def smalltalk_stream():

                yield "You're welcome! 😊"

            return StreamingResponse(
                smalltalk_stream(),
                media_type="text/plain"
            )

        # -------------------------------------------------
        # Retrieval
        # -------------------------------------------------

        top_k = get_top_k(intent)

        rewritten_question = rewrite_question(
            question
        )

        logger.info(
            "Streaming rewritten question: %s",
            rewritten_question
        )

        results = search_documents(
            rewritten_question,
            limit=top_k
        )

        logger.info(
            "Streaming retrieval returned %d chunks",
            len(results)
        )

        # -------------------------------------------------
        # Extract chunks safely
        # -------------------------------------------------

        top_chunks = []

        for result in results:

            if result.payload and "text" in result.payload:

                top_chunks.append(
                    result.payload["text"]
                )

        # -------------------------------------------------
        # Context Compression
        # -------------------------------------------------

        compressed_context = compress_context(
            rewritten_question,
            top_chunks
        )

        logger.info(
            "Streaming context prepared: %d characters",
            len(compressed_context)
        )

        # -------------------------------------------------
        # Conversation history
        # -------------------------------------------------

        history = get_history()

        # -------------------------------------------------
        # Generate stream
        # -------------------------------------------------

        def stream():

            full_answer = ""

            try:

                for token in generate_answer_stream(
                    question=question,
                    context=compressed_context,
                    history=history
                ):

                    full_answer += token

                    yield token

                # -----------------------------------------
                # Save conversation
                # -----------------------------------------

                add_message(
                    "user",
                    question
                )

                add_message(
                    "assistant",
                    full_answer
                )

                logger.info(
                    "Streaming response completed successfully"
                )

            except Exception as e:

                logger.exception(
                    "Streaming generation failed: %s",
                    str(e)
                )

                yield (
                    "\n\n[AutoMind AI encountered an error "
                    "while generating the response.]"
                )

        return StreamingResponse(
            stream(),
            media_type="text/plain"
        )

    except Exception as e:

        logger.exception(
            "Streaming chat request failed: %s",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail="AutoMind AI failed to process the streaming request."
        )