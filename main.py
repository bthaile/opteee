"""
OPTEEE - Options Trading Education Expert
FastAPI Backend with React Frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import uvicorn
from datetime import datetime

from app.services.rag_service import RAGService
from app.models.chat_models import ChatRequest, ChatResponse, HealthResponse

# Check if we're in test mode (no RAG initialization)
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

# Initialize FastAPI app
app = FastAPI(
    title="OPTEEE API",
    description="Options Trading Education Expert - RAG-powered chat API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = None

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG service on startup"""
    global rag_service
    
    if TEST_MODE:
        print("🧪 Starting in TEST MODE - RAG service disabled")
        print(" API endpoints available for testing")
        return
    
    print(" Initializing OPTEEE API...")
    rag_service = RAGService()
    await rag_service.initialize()
    print(" RAG service initialized successfully")

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if not TEST_MODE else "healthy (test mode)",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint for RAG queries"""
    
    if TEST_MODE:
        # Return a test response that demonstrates conversation history processing
        conversation_summary = ""
        if request.conversation_history:
            conversation_summary = f"\n\n[Test Mode] I can see our conversation history with {len(request.conversation_history)} previous messages. "
            if len(request.conversation_history) > 0:
                last_msg = request.conversation_history[-1]
                conversation_summary += f"Your last message was: '{last_msg.content[:50]}...'"
        
        test_answer = f"""[TEST MODE RESPONSE]
        
Thank you for your question: "{request.query}"

Provider: {request.provider}
Number of results requested: {request.num_results}
Format: {request.format}{conversation_summary}

This is a test response to validate the conversation history functionality. In production, this would be answered using the RAG system with options trading knowledge."""

        return ChatResponse(
            answer=test_answer,
            sources="<div class='test-mode'>Test mode - no real sources</div>",
            raw_sources=[],
            timestamp=datetime.now().isoformat()
        )
    
    if not rag_service:
        raise HTTPException(status_code=503, detail="RAG service not initialized")
    
    try:
        # Extract conversation history if provided
        conversation_history = request.conversation_history or []
        
        result = await rag_service.process_query(
            query=request.query,
            provider=request.provider,
            num_results=request.num_results,
            format=request.format,
            conversation_history=conversation_history
        )
        
        # Return clean response
        
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            raw_sources=result["raw_sources"],
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# Serve React static files (if they exist)
if os.path.exists("frontend/build/static"):
    app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
else:
    print("⚠️  Frontend static files not found - serving API only")

@app.get("/")
async def serve_index():
    """Serve the main frontend page"""
    react_build_path = "frontend/build"
    index_file = os.path.join(react_build_path, "index.html")
    
    if os.path.exists(index_file):
        return FileResponse(index_file)
    else:
        # Fallback for development - serve a simple HTML page
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>OPTEEE - Options Trading Education Expert</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <div id="root">
                <h1>OPTEEE API</h1>
                <p>Frontend not built yet. API endpoints available at:</p>
                <ul>
                    <li><a href="/api/health">/api/health</a></li>
                    <li>POST /api/chat</li>
                </ul>
            </div>
        </body>
        </html>
        """

if __name__ == "__main__":
    # For HuggingFace Spaces compatibility
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port) 