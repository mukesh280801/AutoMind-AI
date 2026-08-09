from services.intent_service import detect_intent
from services.retrieval_service import get_top_k
from services.search_service import search_documents
from services.compression_service import compress_context
from services.query_rewrite_service import rewrite_question
from services.llm_service import generate_answer

from services.cache_service import (
    get_cached_answer,
    save_cached_answer
)

from services.metrics_service import Timer

from services.memory_service import (
    add_message,
    get_history
)

from services.logging_service import get_logger


# =========================================================
# Logger
# =========================================================

logger = get_logger("chat_orchestrator")


# =========================================================
# Main Chat Pipeline
# =========================================================

def process_chat(question: str):

    # =====================================================
    # Total Timer
    # =====================================================

    total_timer = Timer()

    logger.info(
        "Question received: %s",
        question
    )

    # =====================================================
    # Intent Detection
    # =====================================================

    intent_timer = Timer()

    intent = detect_intent(question)

    intent_time = intent_timer.elapsed_ms()

    logger.info(
        "Intent detected: %s",
        intent
    )

    # =====================================================
    # Greeting
    # =====================================================

    if intent == "greeting":

        logger.info(
            "Greeting detected"
        )

        return {
            "intent": intent,
            "cached": False,
            "answer": "Hello! 👋 I am AutoMind AI. How can I help you today?"
        }

    # =====================================================
    # Small Talk
    # =====================================================

    if intent == "smalltalk":

        logger.info(
            "Small talk detected"
        )

        return {
            "intent": intent,
            "cached": False,
            "answer": "You're welcome! 😊"
        }

    # =====================================================
    # Cache Check
    # =====================================================

    cache_timer = Timer()

    cached_answer = get_cached_answer(question)

    cache_time = cache_timer.elapsed_ms()

    # -----------------------------------------------------
    # Cache Hit
    # -----------------------------------------------------

    if cached_answer:

        logger.info(
            "Cache hit for question"
        )

        total_time = total_timer.elapsed_ms()

        return {
            "intent": intent,
            "cached": True,
            "question": question,
            "answer": cached_answer,
            "metrics": {
                "intent_time_ms": intent_time,
                "cache_time_ms": cache_time,
                "search_time_ms": 0,
                "compression_time_ms": 0,
                "llm_time_ms": 0,
                "total_time_ms": total_time
            }
        }

    # -----------------------------------------------------
    # Cache Miss
    # -----------------------------------------------------

    logger.info(
        "Cache miss - continuing pipeline"
    )

    # =====================================================
    # Adaptive Retrieval
    # =====================================================

    top_k = get_top_k(intent)

    logger.info(
        "Adaptive retrieval: intent=%s, top_k=%d",
        intent,
        top_k
    )

    # =====================================================
    # Query Rewriting
    # =====================================================

    rewritten_question = rewrite_question(question)

    logger.info(
        "Query rewritten: %s",
        rewritten_question
    )

    # =====================================================
    # Search
    # =====================================================

    search_timer = Timer()

    results = search_documents(
        rewritten_question,
        limit=top_k
    )

    search_time = search_timer.elapsed_ms()

    logger.info(
        "Retrieved %d chunks",
        len(results)
    )

    # =====================================================
    # Get Top Chunks
    # =====================================================

    top_chunks = []

    for result in results[:top_k]:

        if result.payload and "text" in result.payload:

            top_chunks.append(
                result.payload["text"]
            )

    logger.info(
        "Selected %d chunks for context",
        len(top_chunks)
    )

    # =====================================================
    # Context Compression
    # =====================================================

    compression_timer = Timer()

    compressed_context = compress_context(
        rewritten_question,
        top_chunks
    )

    compression_time = compression_timer.elapsed_ms()

    logger.info(
        "Context compression completed: %d characters",
        len(compressed_context)
    )

    # =====================================================
    # Conversation History
    # =====================================================

    history = get_history()

    logger.info(
        "Conversation history loaded: %d messages",
        len(history)
    )

    # =====================================================
    # LLM
    # =====================================================

    logger.info(
        "Sending context to LLM"
    )

    llm_timer = Timer()

    answer = generate_answer(
        question=question,
        context=compressed_context,
        history=history
    )

    llm_time = llm_timer.elapsed_ms()

    logger.info(
        "LLM response generated"
    )

    # =====================================================
    # Save Conversation
    # =====================================================

    add_message(
        "user",
        question
    )

    add_message(
        "assistant",
        answer
    )

    logger.info(
        "Conversation memory updated"
    )

    # =====================================================
    # Save Cache
    # =====================================================

    save_cached_answer(
        question,
        answer
    )

    logger.info(
        "Answer saved to cache"
    )

    # =====================================================
    # Total Time
    # =====================================================

    total_time = total_timer.elapsed_ms()

    logger.info(
        "Chat completed in %.2f ms",
        total_time
    )

    # =====================================================
    # Response
    # =====================================================

    return {
        "intent": intent,
        "cached": False,
        "top_k": top_k,
        "question": question,
        "rewritten_question": rewritten_question,
        "compressed_context": compressed_context,
        "answer": answer,
        "sources": top_chunks,
        "metrics": {
            "intent_time_ms": intent_time,
            "cache_time_ms": cache_time,
            "search_time_ms": search_time,
            "compression_time_ms": compression_time,
            "llm_time_ms": llm_time,
            "total_time_ms": total_time
        }
    }