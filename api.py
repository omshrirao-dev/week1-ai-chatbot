import os
import logging
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
    conversation_history = []
    return {"message": "Conversation reset successfully"}
      






