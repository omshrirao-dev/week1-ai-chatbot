import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Validate API key at startup
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file.")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

# Create Groq client
client = Groq(api_key=api_key)

# Conversation history
conversation_history = []

# System prompt
system_prompt = "You are a helpful assistant. Answer clearly and concisely."


class MessageRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    reply: str


@app.get("/")
def home():
    return {"status": "AI Chatbot API is running"}


@app.post("/chat", response_model=MessageResponse)
def chat(request: MessageRequest):

    # Validate message is not empty
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




