from fastapi import FastAPI
from app.api.chat import router

app = FastAPI(
    title="AI ChatBot",
    version="1.0.0"
)

@app.get("/")
async def home():
    return{
        "message" : "Welcome to AI Chatbot API"
    }

app.include_router(router)    
