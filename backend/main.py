from fastapi import FastAPI
from pydantic import BaseModel

from agents.routing_agent import ask_routing_agent


app = FastAPI(
    title="TechStore AI Customer Support",
    description="AI Customer Support Multi-Agent System",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def home():
    return {
        "message": "TechStore AI Customer Support API is running."
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    answer = ask_routing_agent(request.question)

    return ChatResponse(
        answer=answer
    )

