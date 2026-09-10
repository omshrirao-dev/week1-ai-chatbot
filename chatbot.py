#

import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Create Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Store conversation history
conversation_history = []

# System prompt - tells the AI how to behave
system_prompt = "Suppose you are a research Engineer at the top AI Lab "

print("Chatbot started! Type 'quit' to exit.\n")

# Main conversation loop
while True:
    # Get user input
    user_input = input("You: ")
    
    # Exit if user types quit
    if user_input.lower() == "quit":
        print("Goodbye!")
        break
    
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    # Call Groq API
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=
            [{"role": "system", "content": system_prompt}] + conversation_history,
        max_tokens=1024,
    )
    
    # Extract the response text
    assistant_message = response.choices[0].message.content
    
    # Add assistant response to history
    conversation_history.append({
        "role": "assistant", 
        "content": assistant_message
    })
    
    # Print response
    print(f"\nAssistant: {assistant_message}\n")



""" import os
from groq import Groq

from dotenv import load_dotenv
load_dotenv()
import os
key = os.environ.get("GROQ_API_KEY")
print(f"Key found: {key[:10] if key else 'NOT FOUND'}")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
conversation_history = []

system_prompt = "You are a helpful assistant. Answer clearly and concisely."

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "bye", "q"]:
        print("Goodbye!")
    break

conversation_history.append({
    "role": "user",
    "content": user_input
})

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
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

print(f"\nAssistant: {assistant_message}\n" 
"""
"""  I USED THIS TO CHECK KEY IS FOUND OR NOT 

        load_dotenv()

# TEMPORARY DEBUGGING - remove after fix
import os
key = os.environ.get("GROQ_API_KEY")
print(f"Key found: {key[:10] if key else 'NOT FOUND'}")

CHECK WHICH MODELS ARE AVAILABLE

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# List all available models on your account
models = client.models.list()

print("Models available on your account:")
for model in models.data:
    print(f"  - {model.id}")



    

WORKED SUCCESSFULLY 
    """