import os
import logging
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
client = Groq(api_key=api_key)
conversation_history = []
MAX_HISTORY = 10

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


class MessageRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    reply: str


@app.get("/")
def home():
    return {"status": "AI Chatbot API is running"}

@app.post("/chat", response_model=MessageResponse)
def chat(request: MessageRequest):
    global conversation_history

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    try:
        logger.info(f"Received: {request.message}")

        conversation_history.append({
            "role": "user",
            "content": request.message
        })

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + conversation_history,
            max_tokens=1024,
        )

        assistant_message = response.choices[0].message.content

        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        if len(conversation_history) > MAX_HISTORY:
            conversation_history = conversation_history[-MAX_HISTORY:]

        logger.info(f"Reply sent: {assistant_message[:50]}...")
        return MessageResponse(reply=assistant_message)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if conversation_history and conversation_history[-1]["role"] == "user":
            conversation_history.pop()
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong: {str(e)}"
        )


@app.post("/reset")
def clear():
    global conversation_history

    # Step 1 — Create folder if it does not exist
    history_folder = "chat_histories"
    os.makedirs(history_folder, exist_ok=True)

    # Step 2 — Count existing files to get sequence number
    existing_files = [
        f for f in os.listdir(history_folder)
        if f.startswith("chat_") and f.endswith(".json")
        and f != "index.json"
    ]
    sequence_number = len(existing_files) + 1
    sequence = str(sequence_number).zfill(3)  # 001, 002, 003

    # Step 3 — Save history file if history exists
    if conversation_history:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_{sequence}_{timestamp}.json"
        filepath = os.path.join(history_folder, filename)

        with open(filepath, "w") as f:
            json.dump(conversation_history, f, indent=2)

        logger.info(f"History saved to {filepath}")

        # Step 4 — Update index file
        index_path = os.path.join(history_folder, "index.json")

        # Read existing index or create empty one
        if os.path.exists(index_path):
            with open(index_path, "r") as f:
                index = json.load(f)
        else:
            index = []

        # Add new entry to index
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

        # Clear history
        conversation_history = []

        return {
            "message": f"Conversation reset. Session {sequence} saved.",
            "filename": filename,
            "messages_saved": len(index[-1].get('message_count', 0))
        }

    # If no history to save — just reset
    conversation_history = []
    return {"message": "Conversation reset. No history to save."}