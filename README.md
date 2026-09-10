![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)
![Groq](https://img.shields.io/badge/Groq-API-orange)

# AI Chatbot API

A production-quality AI chatbot built with FastAPI and Groq LLM API.

## What it does
- Accepts messages via REST API
- Maintains conversation history (memory)
- Returns AI-generated responses
- Handles errors gracefully

## Tech stack
- Python
- FastAPI
- Groq API (LLM)
- Pydantic
- Uvicorn

## How to run

1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Create .env file:
   GROQ_API_KEY=your_key_here
4. Start the server:
   python -m uvicorn api:app --reload
5. Visit http://127.0.0.1:8000/docs

## API endpoints

GET  /       → health check
POST /chat   → send message, get AI reply

## What I learned building this
- REST API design with FastAPI
- HTTP methods and status codes
- Error handling and fail-fast pattern
- Environment variables and security
- Pydantic data validation
- Conversation memory with LLMs
