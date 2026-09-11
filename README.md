# AutoMind AI

## AutoMind AI - A RAG-Based Generative AI Workspace for Automotive Engineering Knowledge Retrieval

AutoMind AI is a document-based Generative AI workspace designed to help automotive engineers retrieve and understand technical knowledge from engineering documents.

The system uses Retrieval-Augmented Generation (RAG), LangGraph workflow orchestration, vector search, conversation memory, and grounded LLM responses.

## Key Features

- Engineering PDF document upload
- PDF text extraction and chunking
- Semantic vector embeddings
- Qdrant vector database
- Intent-based query handling
- Query rewriting for follow-up questions
- Top-K document retrieval
- Context compression
- LangGraph workflow orchestration
- Conversation memory
- Grounded document-based responses
- Streaming AI responses
- React + TypeScript interface
- Automotive engineering document retrieval

## RAG Workflow

User Question -> Intent Detection -> Query Rewriting -> Vector Retrieval -> Context Compression -> Grounded LLM Response

## Technology Stack

- React
- TypeScript
- Tailwind CSS
- Vite
- Python
- FastAPI
- LangChain
- LangGraph
- Ollama
- PyMuPDF
- Sentence Transformers
- all-MiniLM-L6-v2
- Qdrant
- SQLite-based LangGraph checkpointing

## Testing

Backend tests: 12/12 passed
Evaluation: 20/20 tests passed (100%)
Frontend production build: successful

## Current Status

Core AutoMind AI RAG functionality is implemented and validated.
