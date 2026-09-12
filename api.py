import os
import json
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# ─────────────────────────────────────────
# STARTUP — load config and validate
# ─────────────────────────────────────────

# Load environment variables from .env file
load_dotenv()

# Fail-fast — crash immediately if API key missing
# Better to fail at startup than mid-request
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file. Server cannot start.")

# Setup logging — makes server activity visible in terminal
# INFO = normal operations | ERROR = something broke
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
# APP SETUP — create app and AI client
# ─────────────────────────────────────────

# FastAPI app — this is the entire web server
app = FastAPI(
    title="AI Mentor Chatbot API",
    description="An AI engineering mentor chatbot built with FastAPI and Groq",
    version="1.0.0"
)

# Groq client — handles all AI API calls
client = Groq(api_key=api_key)

# ─────────────────────────────────────────
# MEMORY — conversation history
# ─────────────────────────────────────────

# Stores all messages in current session
# Each message = {"role": "user/assistant", "content": "..."}
# Shared across all users — fine for learning, fix in production with DB
conversation_history = []

# Sliding window — keeps only last 10 messages
# Prevents hitting token limits in long conversations
MAX_HISTORY = 10

# ─────────────────────────────────────────
# SYSTEM PROMPT — AI personality and rules
# ─────────────────────────────────────────

# This controls everything about how the AI responds
# Change this one string = completely different AI behavior
# This is prompt engineering — a core skill
system_prompt = """You are an AI engineering mentor and friendly guide for students who want to enter the AI field. Your users are undergraduates, graduates, working professionals, and anyone looking to upgrade their career into AI engineering.

Your job is to:
- Give industry-relevant information — always based on what companies actually need today, not generic textbook knowledge
- Provide well-researched, specific answers — never vague or generic
- Give realistic plans and roadmaps — systematic, well thought out, achievable
- Always reflect the current state of the AI industry — real tools, real roles, real expectations

Your tone is like a mentor who is also a friend — honest, direct, encouraging, and practical.

Response style:
- Keep answers concise and to the point — no unnecessary padding
- Use bullet points only when listing multiple items
- Maximum 150 words unless the question genuinely needs more
- If the answer can be said in 3 sentences — say it in 3 sentences

You must never:
- Give false information or false promises
- Sugarcoat the reality of the AI job market
- Give generic advice that sounds good but helps nobody
- Answer questions outside of AI engineering, career guidance, and tech learning

If you don't know something — say so honestly. Always prioritize the student's real career growth over making them feel good."""


# ─────────────────────────────────────────
# DATA MODELS — request and response shapes
# ─────────────────────────────────────────

# Pydantic validates incoming data automatically
# If request does not match this shape — FastAPI returns 422 error
class MessageRequest(BaseModel):
    message: str  # must be a string


# Every response from /chat will always have this shape
# Predictable responses = easier for any frontend or client to use
class MessageResponse(BaseModel):
    reply: str


# ─────────────────────────────────────────
# ROUTES — the API endpoints
# ─────────────────────────────────────────

# Health check — confirms server is alive
# Visit http://127.0.0.1:8000 to see this
@app.get("/")
def home():
    return {
        "status": "AI Mentor Chatbot is running",
        "version": "1.0.0",
        "endpoints": ["/chat", "/reset", "/history"]
    }


# Main chat endpoint — send a message, get AI reply
# POST because we are SENDING data (not just reading)
@app.post("/chat", response_model=MessageResponse)
def chat(request: MessageRequest):

    # Global keyword needed because we ASSIGN to this variable
    # Without global — Python treats it as a local variable and crashes
    global conversation_history

    # ── VALIDATION (before try) ──
    # Business rule: empty messages are not allowed
    # This is OUR intentional check — always before try block
    # Returns 400 (user fault) not 500 (server fault)
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    # ── OPERATIONS (inside try) ──
    # Groq API call might fail for reasons outside our control
    # Network issues, Groq server down, rate limits, expired key
    # try/except handles these unexpected failures gracefully
    try:
        logger.info(f"Received: {request.message}")

        # Add user message to conversation history
        conversation_history.append({
            "role": "user",
            "content": request.message
        })

        # Call Groq API with full conversation history
        # System prompt + history = AI has full context
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + conversation_history,
            max_tokens=1024,
        )

        # Extract just the text from the API response object
        assistant_message = response.choices[0].message.content

        # Add AI reply to history so next message has full context
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        # Sliding window — drop oldest messages when limit exceeded
        # Prevents token limit errors in long conversations
        if len(conversation_history) > MAX_HISTORY:
            conversation_history = conversation_history[-MAX_HISTORY:]

        logger.info(f"Reply sent: {assistant_message[:50]}...")
        return MessageResponse(reply=assistant_message)

    except Exception as e:
        # Log the actual error for debugging
        logger.error(f"Error: {str(e)}")

        # Rollback — remove the failed user message from history
        # Without this: history has user message but no reply
        # That broken state confuses AI on the next request
        if conversation_history and conversation_history[-1]["role"] == "user":
            conversation_history.pop()

        # Raise HTTP 500 — server side problem, not user's fault
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong: {str(e)}"
        )


# Reset endpoint — clear conversation history
# Saves history to file before clearing so nothing is lost
@app.post("/reset")
def clear():
    global conversation_history

    # Create folder to store all chat histories
    # exist_ok=True means don't crash if folder already exists
    history_folder = "chat_histories"
    os.makedirs(history_folder, exist_ok=True)

    # Count existing files to get sequence number
    # Filters only chat files, excludes index.json
    existing_files = [
        f for f in os.listdir(history_folder)
        if f.startswith("chat_") and f.endswith(".json")
        and f != "index.json"
    ]
    sequence_number = len(existing_files) + 1

    # zfill(3) pads with zeros: 1 → "001", 12 → "012"
    # Keeps files sorted correctly in folder
    sequence = str(sequence_number).zfill(3)

    # Only save if there is actual history to save
    if conversation_history:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_{sequence}_{timestamp}.json"
        filepath = os.path.join(history_folder, filename)

        # Write conversation history to JSON file
        with open(filepath, "w") as f:
            json.dump(conversation_history, f, indent=2)

        logger.info(f"History saved to {filepath}")

        # Update index file — master list of all sessions
        index_path = os.path.join(history_folder, "index.json")

        # Read existing index or start fresh
        if os.path.exists(index_path):
            with open(index_path, "r") as f:
                index = json.load(f)
        else:
            index = []

        # Add this session to the index
        index.append({
            "sequence": sequence_number,
            "filename": filename,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_count": len(conversation_history)
        })

        # Save updated index
        with open(index_path, "w") as f:
            json.dump(index, f, indent=2)

        logger.info(f"Index updated — session {sequence}")

        # Clear history after saving
        conversation_history = []

        return {
            "message": f"Conversation reset. Session {sequence} saved.",
            "filename": filename,
            "messages_saved": index[-1]["message_count"]
        }

    # If no history — just reset silently
    conversation_history = []
    return {"message": "Conversation reset. No history to save."}


# History endpoint — see current conversation (bonus endpoint)
# Useful for debugging and understanding what AI sees
@app.get("/history")
def get_history():
    return {
        "message_count": len(conversation_history),
        "max_history": MAX_HISTORY,
        "conversation": conversation_history
    }