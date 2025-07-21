"""
Simple health server for HuggingFace Spaces
Runs alongside the Discord bot to provide health monitoring
"""
import os
import asyncio
import json
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

# Create FastAPI app
app = FastAPI(title="OPTEEE Discord Bot Health Server")

# Track bot status
bot_status = {
    "status": "starting",
    "last_seen": None,
    "uptime_start": datetime.now().isoformat(),
    "message": "Discord bot is initializing..."
}

@app.get("/health")
async def health_check():
    """Health check endpoint for HuggingFace Spaces"""
    return {
        "status": "healthy",
        "service": "OPTEEE Discord Bot",
        "timestamp": datetime.now().isoformat(),
        "bot_status": bot_status["status"],
        "message": bot_status["message"]
    }

@app.get("/")
async def root():
    """Root endpoint showing bot status"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OPTEEE Discord Bot</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 40px; }}
            .status-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .status-healthy {{ border-left: 4px solid #28a745; }}
            .status-warning {{ border-left: 4px solid #ffc107; }}
            .code {{ background: #e9ecef; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
        </style>
    </head>
    <body>
        <h1>🤖 OPTEEE Discord Bot</h1>
        <p>This Discord bot provides access to the OPTEEE options trading knowledge base.</p>
        
        <div class="status-card status-healthy">
            <h3>✅ Service Status</h3>
            <p><strong>Status:</strong> {bot_status["status"].title()}</p>
            <p><strong>Message:</strong> {bot_status["message"]}</p>
            <p><strong>Uptime Since:</strong> {bot_status["uptime_start"]}</p>
        </div>
        
        <h3>📋 Available Commands</h3>
        <ul>
            <li><span class="code">!search &lt;query&gt;</span> - Search with transcript excerpts, timestamps, and clickable video links</li>
            <li><span class="code">!search_advanced &lt;num_results&gt; &lt;query&gt;</span> - Advanced search with custom result count</li>
            <li><span class="code">!health</span> - Check API health status</li>
            <li><span class="code">!show_help</span> - Show all commands</li>
        </ul>
        
        <h3>🔗 Connect to Discord</h3>
        <p>Invite this bot to your Discord server to start searching options trading information!</p>
        
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; font-size: 0.9em;">
            <p>This bot connects to the main OPTEEE API at: <br>
            <span class="code">{os.getenv('OPTEEE_API_URL', 'https://bthaile-opteee.hf.space')}</span></p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/status")
async def get_status():
    """Detailed status endpoint"""
    return bot_status

def update_bot_status(status: str, message: str):
    """Update bot status from Discord bot"""
    bot_status["status"] = status
    bot_status["message"] = message
    bot_status["last_seen"] = datetime.now().isoformat()

async def run_health_server():
    """Run the health server"""
    port = int(os.getenv("PORT", 8080))
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    # Run the health server
    asyncio.run(run_health_server()) 