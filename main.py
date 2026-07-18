"""
OPTEEE - Options Trading Education Expert
FastAPI Backend with React Frontend
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import uvicorn
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.rag_service import RAGService
from app.models.chat_models import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    PDFExtractRequest,
    PDFExtractResponse,
    ConversationDetail,
    ConversationSummary,
    ConversationMessage,
)
from app.db.init_db import init_db
from app.db.database import get_db
from app.services.conversation_service import ConversationService
from app.services.history_utils import sanitize_history_content
from app.services.pdf_extractor_service import PDFExtractorService
from app.services import wiki_service

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
pdf_extractor_service = PDFExtractorService()

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG service on startup"""
    global rag_service
    init_db()
    
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


@app.post("/api/pdf/extract", response_model=PDFExtractResponse)
async def extract_pdf_endpoint(request: PDFExtractRequest):
    """Extract a local PDF using the pipeline venv and routed baseline/Marker backends."""
    try:
        payload = pdf_extractor_service.extract(
            request.pdf_path,
            backend=request.backend,
            allow_ocr=request.allow_ocr,
            marker_command=request.marker_command,
        )
        return PDFExtractResponse(ok=True, payload=payload)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/help")
async def api_help():
    """Machine-readable capability guide for external agents and integrations."""
    return {
        "name": "OPTEEE API",
        "version": "1.0.0",
        "purpose": "Options Trading Education Expert - RAG chat API with persisted conversations and a synthesized wiki/knowledge layer.",
        "formats": {
            "chat_formats": {
                "html": "Browser-oriented answer plus formatted HTML sources.",
                "json": "Agent/bot-oriented answer with structured raw_sources and wiki_references.",
                "bot": "Alias of json for bot clients."
            },
            "wiki_page_formats": {
                "html": "Rendered HTML page payload for browser use.",
                "markdown": "Raw markdown payload for agent analysis.",
                "json": "Combined structured page payload with frontmatter, markdown, html, and wikilinks."
            }
        },
        "capabilities": {
            "chat": [
                "RAG question answering over options-trading transcripts and research PDFs.",
                "Structured citations via raw_sources.",
                "Top-level wiki_references synthesized from retrieved sources.",
                "Conversation persistence via conversation_id.",
                "Optional provider, model, effort, and num_results controls."
            ],
            "conversations": [
                "Create a new persisted conversation.",
                "Reuse a conversation across turns with conversation_id.",
                "List recent conversations.",
                "Fetch a full conversation transcript.",
                "Delete a conversation."
            ],
            "wiki": [
                "Fetch the graph-backed wiki index as structured JSON.",
                "Fetch individual wiki pages as markdown, html, or combined json.",
                "Traverse knowledge relationships through wikilinks and graph edges.",
                "Drill down from chat responses into related synthesized wiki pages."
            ],
            "pdf_extraction": [
                "Route local PDFs through baseline or Marker extraction.",
                "Return provenance, quality scores, and extracted markdown in one payload.",
                "Use the pipeline venv so serving stays decoupled from heavy PDF dependencies."
            ]
        },
        "endpoints": [
            {
                "path": "/api/health",
                "method": "GET",
                "purpose": "Health check",
                "returns": ["status", "timestamp", "version"]
            },
            {
                "path": "/api/pdf/extract",
                "method": "POST",
                "purpose": "Extract one local PDF through the routed PDF processor service",
                "returns": ["ok", "payload.backend_used", "payload.route_reason", "payload.quality", "payload.markdown"]
            },
            {
                "path": "/api/help",
                "method": "GET",
                "purpose": "Machine-readable capability guide for agents",
                "returns": ["capabilities", "endpoints", "workflows", "examples"]
            },
            {
                "path": "/api/chat",
                "method": "POST",
                "purpose": "Main RAG chat endpoint",
                "returns": ["answer", "sources", "raw_sources", "wiki_references", "conversation_id", "token_usage"]
            },
            {
                "path": "/api/conversations",
                "method": "POST",
                "purpose": "Create a new persisted conversation",
                "returns": ["id", "title", "created_at", "updated_at"]
            },
            {
                "path": "/api/conversations?limit=20",
                "method": "GET",
                "purpose": "List recent conversations",
                "returns": ["id", "title", "created_at", "updated_at"]
            },
            {
                "path": "/api/conversations/{conversation_id}",
                "method": "GET",
                "purpose": "Fetch one conversation with full message history",
                "returns": ["id", "title", "messages[]"]
            },
            {
                "path": "/api/conversations/{conversation_id}",
                "method": "DELETE",
                "purpose": "Delete one persisted conversation",
                "returns": ["ok"]
            },
            {
                "path": "/api/wiki/index/document",
                "method": "GET",
                "purpose": "Structured JSON form of the generated wiki/index.md entrypoint",
                "returns": ["path", "frontmatter", "markdown", "wikilinks"]
            },
            {
                "path": "/api/wiki/index",
                "method": "GET",
                "purpose": "Lightweight wiki catalog for browse/search",
                "returns": ["page_count", "source_count", "pages", "sources"]
            },
            {
                "path": "/api/wiki/graph.json",
                "method": "GET",
                "purpose": "Knowledge graph topology",
                "returns": ["nodes", "edges"]
            },
            {
                "path": "/api/wiki/pages/{path}?format=json",
                "method": "GET",
                "purpose": "Fetch one wiki page with frontmatter, markdown, html, and wikilinks",
                "returns": ["path", "frontmatter", "markdown", "html", "wikilinks"]
            },
            {
                "path": "/wiki/page/{path}",
                "method": "GET",
                "purpose": "Standalone rendered wiki page view",
                "returns": ["html_document"]
            },
            {
                "path": "/openapi.json",
                "method": "GET",
                "purpose": "Formal OpenAPI schema for strict machine clients",
                "returns": ["openapi", "paths", "components"]
            }
        ],
        "request_shapes": {
            "chat": {
                "required": ["query"],
                "optional": ["provider", "model", "effort", "num_results", "format", "conversation_history", "conversation_id"],
                "example": {
                    "query": "What is a covered strangle?",
                    "provider": "claude",
                    "num_results": 5,
                    "format": "json"
                }
            }
        },
        "response_fields": {
            "chat": {
                "answer": "Primary plain-text answer.",
                "sources": "Formatted sources string for the selected response format.",
                "raw_sources": "Structured source/citation objects.",
                "wiki_references": "Deduped synthesized wiki pages related to the retrieved sources.",
                "conversation_id": "Conversation identifier to persist and reuse.",
                "token_usage": "Provider/model token usage for the answer when available."
            },
            "wiki_reference": {
                "path": "Wiki page path, e.g. concepts/portfolio-first.",
                "category": "High-level page category, e.g. concept or strategy.",
                "label": "Human-readable title.",
                "url": "Relative browser URL for standalone wiki page view."
            }
        },
        "workflows": {
            "simple_chat": [
                "Call POST /api/chat with format=json or format=bot.",
                "Show answer to the user.",
                "Optionally render raw_sources as citations."
            ],
            "conversation_chat": [
                "Create a conversation with POST /api/conversations.",
                "Store the returned id as conversation_id.",
                "Send conversation_id on each POST /api/chat.",
                "Persist the conversation_id returned by the chat response."
            ],
            "chat_to_wiki_drilldown": [
                "Call POST /api/chat with format=json.",
                "Inspect response wiki_references[].",
                "Fetch one or more pages with GET /api/wiki/pages/{path}?format=json.",
                "Use page frontmatter, markdown, html, and wikilinks for deeper follow-up."
            ],
            "open_ended_research": [
                "Fetch GET /api/wiki/index/document as the knowledge-layer entrypoint.",
                "Follow wikilinks or graph relationships from GET /api/wiki/graph.json.",
                "Fetch detailed pages with GET /api/wiki/pages/{path}?format=json."
            ]
        },
        "examples": {
            "chat_to_wiki": {
                "step_1": {
                    "method": "POST",
                    "path": "/api/chat",
                    "body": {
                        "query": "Teach one short lesson on portfolio-first trade evaluation.",
                        "provider": "claude",
                        "num_results": 5,
                        "format": "json"
                    }
                },
                "step_2": "Read answer and wiki_references from the chat response.",
                "step_3": {
                    "method": "GET",
                    "path": "/api/wiki/pages/concepts/portfolio-first?format=json"
                }
            }
        },
        "notes": [
            "Use /openapi.json for strict machine schema discovery.",
            "Use /api/help for practical workflow guidance.",
            "Use format=json or format=bot for external agent integrations.",
            "When a conversation_id is supplied, server-side persisted history is the source of truth."
        ]
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Main chat endpoint for RAG queries"""
    
    if TEST_MODE:
        # Return a deterministic response while still exercising conversation persistence.
        conversation = None
        if request.conversation_id:
            conversation = ConversationService.get_conversation(db, request.conversation_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = ConversationService.create_conversation(db)

        ConversationService.add_message(db, conversation, "user", request.query)

        conversation_summary = ""
        if request.conversation_history:
            conversation_summary = f"\n\n[Test Mode] I can see our conversation history with {len(request.conversation_history)} previous messages. "
            if len(request.conversation_history) > 0:
                last_msg = request.conversation_history[-1]
                conversation_summary += f"Your last message was: '{last_msg.content[:50]}...'"
        
        test_answer = f"""[TEST MODE RESPONSE]
        
Thank you for your question: "{request.query}"

Provider: {request.provider}
Model: {request.model or '[default]'}
Effort: {request.effort}
Number of results requested: {request.num_results}
Format: {request.format}{conversation_summary}

This is a test response to validate the conversation history functionality. In production, this would be answered using the RAG system with options trading knowledge."""

        ConversationService.add_message(db, conversation, "assistant", test_answer)

        return ChatResponse(
            answer=test_answer,
            sources="[]",
            raw_sources=[],
            wiki_references=[],
            timestamp=datetime.now().isoformat(),
            conversation_id=conversation.id,
            token_usage={
                "provider": request.provider,
                "model": request.model or "[default]",
                "effort": request.effort,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            },
        )
    
    if not rag_service:
        raise HTTPException(status_code=503, detail="RAG service not initialized")
    
    try:
        # Resolve or create persisted conversation for this chat turn.
        conversation = None
        if request.conversation_id:
            conversation = ConversationService.get_conversation(db, request.conversation_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = ConversationService.create_conversation(db)

        # Persist user message first.
        ConversationService.add_message(db, conversation, "user", request.query)

        # Prefer server-side history when conversation_id is present.
        if request.conversation_id:
            refreshed = ConversationService.get_conversation(db, conversation.id)
            history_messages = refreshed.messages if refreshed else []
            conversation_history = [
                ConversationMessage(
                    role=m.role,
                    content=sanitize_history_content(m.role, m.content),
                    timestamp=m.created_at.isoformat(),
                )
                for m in history_messages[:-1]  # exclude current user message
            ]
        else:
            conversation_history = request.conversation_history or []

        result = await rag_service.process_query(
            query=request.query,
            provider=request.provider,
            model=request.model,
            effort=request.effort,
            num_results=request.num_results,
            format=request.format,
            conversation_history=conversation_history
        )

        # Persist assistant output (answer + formatted sources for replay).
        assistant_content = result["answer"] + (result.get("sources") or "")
        ConversationService.add_message(db, conversation, "assistant", assistant_content)
        
        # Return clean response
        
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            raw_sources=result["raw_sources"],
            wiki_references=result.get("wiki_references", []),
            timestamp=datetime.now().isoformat(),
            conversation_id=conversation.id,
            token_usage=result.get("token_usage"),
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/api/conversations", response_model=ConversationSummary)
async def create_conversation(db: Session = Depends(get_db)):
    conversation = ConversationService.create_conversation(db)
    return ConversationSummary(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at.isoformat(),
        updated_at=conversation.updated_at.isoformat(),
    )


@app.get("/api/conversations", response_model=List[ConversationSummary])
async def list_conversations(limit: int = 20, db: Session = Depends(get_db)):
    safe_limit = max(1, min(limit, 100))
    conversations = ConversationService.list_conversations(db, limit=safe_limit)
    return [
        ConversationSummary(
            id=c.id,
            title=c.title,
            created_at=c.created_at.isoformat(),
            updated_at=c.updated_at.isoformat(),
        )
        for c in conversations
    ]


@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Delete a conversation and its messages."""
    deleted = ConversationService.delete_conversation(db, conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"ok": True}


@app.get("/api/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conversation = ConversationService.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return ConversationDetail(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at.isoformat(),
        updated_at=conversation.updated_at.isoformat(),
        messages=[
            ConversationMessage(
                role=m.role,
                content=m.content,
                timestamp=m.created_at.isoformat(),
            )
            for m in conversation.messages
        ],
    )

# ---------------------------------------------------------------------------
# Wiki browse/graph layer (Phase-2). Pure filesystem reads over wiki/ — these
# routes do not touch the RAG service and work in TEST_MODE.
# ---------------------------------------------------------------------------
@app.get("/wiki")
async def serve_wiki_graph():
    """Serve the interactive wiki graph browser (WIKI_SCHEMA §8)."""
    wiki_page = "templates/wiki_graph.html"
    if os.path.exists(wiki_page):
        return FileResponse(wiki_page, media_type="text/html")
    raise HTTPException(status_code=404, detail="Wiki graph page not found")


@app.get("/api/wiki/graph.json")
async def wiki_graph_json():
    """Baked knowledge graph (nodes+edges); empty graph if not built yet."""
    return wiki_service.get_graph()


@app.get("/api/wiki/index")
async def wiki_index():
    """Wiki catalog: knowledge pages + source-page list."""
    return wiki_service.list_index()


@app.get("/api/wiki/index/document")
async def wiki_index_document(include_html: bool = False):
    """Generated wiki/index.md as structured JSON for agent analysis."""
    document = wiki_service.get_index_document(include_html=include_html)
    if document is None:
        raise HTTPException(status_code=404, detail="Wiki index document not found")
    return document


@app.get("/api/wiki/pages/{rel_path:path}")
async def wiki_page(rel_path: str, output_format: str = Query("html", alias="format")):
    """Wiki page as JSON.

    format=html keeps the legacy shape for the browser.
    format=markdown returns raw Markdown for agents.
    format=json returns both Markdown and rendered HTML plus structured wikilinks.
    """
    if output_format not in {"html", "markdown", "json"}:
        raise HTTPException(status_code=400, detail="format must be html, markdown, or json")
    page = wiki_service.get_page(
        rel_path,
        include_markdown=output_format in {"markdown", "json"},
        include_html=output_format in {"html", "json"},
    )
    if page is None:
        raise HTTPException(status_code=404, detail="Wiki page not found")
    return page


@app.get("/wiki/page/{rel_path:path}", response_class=HTMLResponse)
async def wiki_page_view(rel_path: str):
    """Standalone rendered wiki page — the target of chat 'Wiki References' links."""
    html_doc = wiki_service.render_page_html(rel_path)
    if html_doc is None:
        raise HTTPException(status_code=404, detail="Wiki page not found")
    return HTMLResponse(content=html_doc)


# Serve favicon.ico
@app.get("/favicon.ico")
async def serve_favicon():
    """Serve the favicon (ICO preferred, SVG fallback)."""
    ico_path = "favicon.ico"
    svg_path = "favicon.svg"

    if os.path.exists(ico_path):
        return FileResponse(ico_path, media_type="image/x-icon")
    if os.path.exists(svg_path):
        return FileResponse(svg_path, media_type="image/svg+xml")
    raise HTTPException(status_code=404, detail="Favicon not found")


@app.get("/favicon.svg")
async def serve_favicon_svg():
    """Serve the SVG favicon directly."""
    svg_path = "favicon.svg"
    if os.path.exists(svg_path):
        return FileResponse(svg_path, media_type="image/svg+xml")
    raise HTTPException(status_code=404, detail="Favicon SVG not found")

# Serve React static files (if they exist)
if os.path.exists("frontend/build/static"):
    app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
else:
    print("⚠️  Frontend static files not found - serving API only")

# Vendored local assets (e.g. static/vendor/cytoscape.min.js for the /wiki graph —
# no external CDN, matching the no-external-calls design). Hardening §15 #9.
if os.path.isdir("static"):
    app.mount("/assets", StaticFiles(directory="static"), name="assets")

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
