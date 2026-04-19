from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
from dotenv import load_dotenv
import os
from schema import Input

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for development (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def status():
    return {
        "status" : "success",
        "message" : "server running"
    }

@app.post("/chat")
def chat(input : Input):
    try:
        response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        data=json.dumps({
            "model": "google/gemma-4-26b-a4b-it:free",
            "messages": [
                {
                    "role": "system",
                    "content": "You are Gemma model developed by google. Return each response in markdown text"
                },
                {
                    "role": "user",
                    "content": input.content
                }
            ]
        })
        )

        data = response.json()
        return {
        "message": data["choices"][0]["message"]["content"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=429)

    