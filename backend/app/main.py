
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.app.services.rag_service import generate_rag_response


# Create FastAPI application
app = FastAPI(
    title="ASUS Support AI",
    description="RAG-powered ASUS laptop technical support chatbot",
    version="1.0.0"
)


# Request structure
class ChatRequest(BaseModel):
    message: str


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "ASUS Support AI backend is running!"
    }


# Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):

    try:
        result = generate_rag_response(request.message)

        return {
            "user_message": request.message,
            "reply": result["answer"],
            "sources": result["sources"]
        }

    except Exception as error:
        print(f"RAG error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Unable to generate AI response."
        )
