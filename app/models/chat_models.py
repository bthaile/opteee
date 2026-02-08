"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ConversationMessage(BaseModel):
    """Model for individual conversation messages"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'", pattern="^(user|assistant)$")
    content: str = Field(..., description="Message content", min_length=1)
    timestamp: str = Field(..., description="Message timestamp in ISO format")

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    query: str = Field(..., description="User's question", min_length=1)
    provider: str = Field(default="claude", description="LLM provider to use")
    num_results: int = Field(default=10, description="Number of search results to retrieve", ge=1, le=20)
    format: str = Field(default="html", description="Response format: 'html' or 'discord'", pattern="^(html|discord)$")
    conversation_history: Optional[List[ConversationMessage]] = Field(
        default=None, 
        description="Optional conversation history for context"
    )

class Source(BaseModel):
    """Model for source information (video or PDF)"""
    title: str = Field(..., description="Source title")
    content: str = Field(..., description="Source content/transcript")
    
    # Source type identifier (default 'video' for backwards compatibility)
    source_type: Optional[str] = Field(default="video", description="Source type: 'video' or 'pdf'")
    
    # Video-specific fields (optional for PDF sources)
    url: Optional[str] = Field(default="", description="Base video URL")
    video_url_with_timestamp: Optional[str] = Field(default="", description="Video URL with timestamp")
    video_id: Optional[str] = Field(default="", description="YouTube video ID")
    upload_date: Optional[str] = Field(default="", description="Upload/publication date")
    duration_seconds: Optional[float] = Field(default=0, description="Video duration in seconds")
    start_timestamp_seconds: Optional[float] = Field(default=0, description="Start timestamp for relevant segment")
    start_timestamp: Optional[str] = Field(default="", description="Formatted timestamp string")
    channel: Optional[str] = Field(default="", description="Channel name")
    
    # PDF-specific fields (optional for video sources)
    document_id: Optional[str] = Field(default="", description="PDF document ID")
    source_file: Optional[str] = Field(default="", description="PDF filename")
    page_number: Optional[int] = Field(default=0, description="Page number in PDF")
    page_range: Optional[str] = Field(default="", description="Page range string")
    section: Optional[str] = Field(default="", description="Section name in PDF")
    author: Optional[str] = Field(default="", description="PDF author")
    
    # Common fields
    score: Optional[float] = Field(default=0.0, description="Relevance score")
    chunk_index: Optional[int] = Field(default=0, description="Chunk index")

# Backwards compatibility alias
VideoSource = Source

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str = Field(..., description="RAG-generated answer")
    sources: str = Field(..., description="Formatted HTML sources")
    raw_sources: List[Dict[str, Any]] = Field(default=[], description="Raw source data (video and PDF)")
    timestamp: str = Field(..., description="Response timestamp")

class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    timestamp: str = Field(..., description="Error timestamp") 