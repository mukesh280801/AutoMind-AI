from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import StreamingResponse

from services.logging_service import get_logger


# =========================================================
# V1 IMPORTS
# =========================================================

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


# =========================================================
# V2 IMPORTS
# =========================================================

from services.graph.chat_service import (
    process_graph_chat,
    stream_graph_chat
)


# =========================================================
# LOGGER
# =========================================================

logger = get_logger("automind.api.chat")


# =========================================================
# ROUTER
# =========================================================

router = APIRouter()


# =========================================================
# REQUEST MODELS
# =========================================================

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )


class V2ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )

    thread_id: str = Field(
        default="default",
        min_length=1,
        max_length=200
    )


# =========================================================
# V1 - NORMAL CHAT
# =========================================================

@router.post("/api/chat")
async def chat(request: ChatRequest):

    try:

        logger.info(
            "V1 chat request: %s",
            request.question
        )

        result = process_chat(
            request.question
        )

        return result

    except Exception as exc:

        logger.exception(
            "V1 chat failed"
        )

        raise HTTPException(
            status_code=500,
            detail="AutoMind AI failed to process the request."
        ) from exc


# =========================================================
# V1 - STREAMING CHAT
# =========================================================

@router.post("/api/chat/stream")
async def stream_chat(request: ChatRequest):

    try:

        intent = detect_intent(
            request.question
        )

        top_k = get_top_k(
            intent
        )

        rewritten_question = rewrite_question(
            request.question
        )

        results = search_documents(
            rewritten_question,
            limit=top_k
        )

        top_chunks = [
            result.payload["text"]
            for result in results
        ]

        compressed_context = compress_context(
            rewritten_question,
            top_chunks
        )

        history = get_history()

    except Exception as exc:

        logger.exception(
            "V1 streaming preparation failed"
        )

        raise HTTPException(
            status_code=500,
            detail="AutoMind AI failed to prepare the request."
        ) from exc

    def stream():

        full_answer = ""

        try:

            for token in generate_answer_stream(
                question=request.question,
                context=compressed_context,
                history=history
            ):

                full_answer += token

                yield token

            add_message(
                "user",
                request.question
            )

            add_message(
                "assistant",
                full_answer
            )

            logger.info(
                "V1 streaming completed"
            )

        except Exception:

            logger.exception(
                "V1 streaming generation failed"
            )

            yield "\n\n[AutoMind AI error: response generation failed.]"

    return StreamingResponse(
        stream(),
        media_type="text/plain"
    )


# =========================================================
# V2 - LANGGRAPH CHAT
# =========================================================

@router.post("/api/v2/chat")
async def chat_v2(request: V2ChatRequest):

    try:

        logger.info(
            "V2 chat request | thread=%s",
            request.thread_id
        )

        result = process_graph_chat(
            question=request.question,
            thread_id=request.thread_id
        )

        return {
            "version": "v2",
            "thread_id": request.thread_id,
            "question": request.question,
            "intent": result.get("intent"),
            "answer": result.get("answer", "")
        }

    except Exception as exc:

        logger.exception(
            "V2 chat failed | thread=%s",
            request.thread_id
        )

        raise HTTPException(
            status_code=500,
            detail="AutoMind AI failed to process the V2 request."
        ) from exc


# =========================================================
# V2 - LANGGRAPH STREAMING CHAT
# =========================================================

@router.post("/api/v2/chat/stream")
async def stream_chat_v2(request: V2ChatRequest):

    logger.info(
        "V2 streaming request | thread=%s",
        request.thread_id
    )

    def stream():

        try:

            for token in stream_graph_chat(
                question=request.question,
                thread_id=request.thread_id
            ):

                yield token

            logger.info(
                "V2 streaming completed | thread=%s",
                request.thread_id
            )

        except Exception:

            logger.exception(
                "V2 streaming failed | thread=%s",
                request.thread_id
            )

            yield "\n\n[AutoMind AI error: response generation failed.]"

    return StreamingResponse(
        stream(),
        media_type="text/plain"
    )