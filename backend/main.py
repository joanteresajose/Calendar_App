import os
# Write service_account.json from environment variable if present
if os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"):
    with open("service_account.json", "w") as f:
        f.write(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModelimport os
# Write service_account.json from environment variable if present
if os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"):
    with open("backend/service_account.json", "w") as f:
        f.write(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, Any
from .agent import agent_respond

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None  # Optional, for multi-turn
    session_state: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None
    session_state: Optional[Dict[str, Any]] = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    user_message = chat_request.message
    session_state = chat_request.session_state or {}
    agent_result = agent_respond(user_message, session_state)
    return ChatResponse(
        response=agent_result["response"],
        session_id=chat_request.session_id,
        session_state=agent_result.get("session_state", {})
    )

@app.get("/chat")
async def chat_get():
    return {"message": "Use POST with a JSON body to interact with this endpoint."}

from typing import Dict, Optional, Any
from agent import agent_respond

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None  # Optional, for multi-turn
    session_state: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None
    session_state: Optional[Dict[str, Any]] = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    user_message = chat_request.message
    session_state = chat_request.session_state or {}
    agent_result = agent_respond(user_message, session_state)
    return ChatResponse(
        response=agent_result["response"],
        session_id=chat_request.session_id,
        session_state=agent_result.get("session_state", {})
    )
