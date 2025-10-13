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

class VideoSource(BaseModel):
    """Model for video source information"""
    title: str = Field(..., description="Video title")
    url: str = Field(..., description="Base video URL")
    video_url_with_timestamp: str = Field(..., description="Video URL with timestamp")
    upload_date: str = Field(..., description="Video upload date")
    duration_seconds: float = Field(..., description="Video duration in seconds")
    start_timestamp_seconds: float = Field(..., description="Start timestamp for relevant segment")
    content: str = Field(..., description="Transcript content")

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str = Field(..., description="RAG-generated answer")
    sources: str = Field(..., description="Formatted HTML sources")
    raw_sources: List[VideoSource] = Field(default=[], description="Raw source data")
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