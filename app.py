"""
FastAPI AI Chatbot for Azure Container Apps Blue-Green Deployment Demo

A simple AI chatbot application that demonstrates Azure Container Apps 
blue-green deployment capabilities with Azure Developer CLI (azd).
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Environment configuration
PORT = int(os.getenv("PORT", "8000"))
REVISION_NAME = os.getenv("CONTAINER_APP_REVISION", "unknown")

# Parse commit ID from revision name (format: web--<commitid>)
if REVISION_NAME != "unknown" and "--" in REVISION_NAME:
    REVISION_COMMIT_ID = REVISION_NAME.split("--", 1)[1]
else:
    REVISION_COMMIT_ID = "unknown"

# For simple deployment stage detection, check if we're the latest revision
# In a real scenario, you'd query the ingress traffic config or use labels
# For now, we'll use a simple heuristic based on environment variable if available
DEPLOYMENT_STAGE = os.getenv("DEPLOYMENT_STAGE", "unknown")

# If not set, try to determine from revision name patterns
if DEPLOYMENT_STAGE == "unknown":
    # This is a simplified detection - in production you'd query the actual traffic labels
    DEPLOYMENT_STAGE = "blue" if REVISION_COMMIT_ID else "unknown"

# FastAPI app initialization
app = FastAPI(
    title="Blue-Green Deployment Demo",
    description="A simple web application to demonstrate Azure Container Apps blue-green deployments",
    version=REVISION_COMMIT_ID if REVISION_COMMIT_ID != "unknown" else "1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    revision: str
    version: str
    uptime_seconds: Optional[int] = None



# App startup time for health checks
startup_time = datetime.now()

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve a simple web interface showing deployment information."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blue-Green Deployment Demo</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                max-width: 900px; 
                margin: 0 auto; 
                padding: 40px 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }}
            .container {{ 
                background: white; 
                border-radius: 12px; 
                padding: 40px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }}
            h1 {{ 
                color: #2c3e50; 
                text-align: center; 
                margin-bottom: 10px;
                font-size: 2.5rem;
            }}
            .subtitle {{
                text-align: center;
                color: #7f8c8d;
                margin-bottom: 40px;
                font-size: 1.1rem;
            }}
            .info-grid {{ 
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .info-card {{ 
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 25px; 
                border-radius: 8px; 
                border-left: 4px solid #007bff;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .info-card.stage-blue {{
                border-left: 4px solid #007bff;
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            }}
            .info-card.stage-green {{
                border-left: 4px solid #28a745;
                background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
            }}
            .stage-badge-blue {{
                color: #0056b3 !important;
                background: #007bff;
                color: white !important;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 1.1rem !important;
                display: inline-block;
            }}
            .stage-badge-green {{
                color: #1e7e34 !important;
                background: #28a745;
                color: white !important;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 1.1rem !important;
                display: inline-block;
            }}
            .info-card h3 {{ 
                margin: 0 0 10px 0; 
                color: #495057; 
                font-size: 1.1rem;
            }}
            .info-card .value {{ 
                font-size: 1.3rem; 
                font-weight: bold; 
                color: #007bff;
                font-family: 'Courier New', monospace;
            }}
            .status-indicator {{
                display: inline-block;
                width: 12px;
                height: 12px;
                background-color: #28a745;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
                100% {{ opacity: 1; }}
            }}
            .actions {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 30px 0;
            }}
            .btn {{
                padding: 15px 25px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                text-align: center;
                font-weight: 500;
                transition: all 0.3s ease;
                display: block;
            }}
            .btn:hover {{
                background: #0056b3;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,123,255,0.3);
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #dee2e6;
                color: #6c757d;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔄 Azure Container Apps - v2 </h1>
            <p class="subtitle">Blue-Green Deployment Demonstration</p>
            
            {'<div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 30px; text-align: center; font-size: 1.2rem; font-weight: bold;">✨ NEW FEATURE: Enhanced deployment info display! ✨</div>' if DEPLOYMENT_STAGE == 'green' else ''}
            
            <div class="info-grid">
                <div class="info-card">
                    <h3>� Commit ID</h3>
                    <div class="value">{REVISION_COMMIT_ID}</div>
                </div>
                <div class="info-card">
                    <h3>🏷️ Revision</h3>
                    <div class="value">{REVISION_NAME}</div>
                </div>
                <div class="info-card stage-{DEPLOYMENT_STAGE}">
                    <h3>� Deployment Stage</h3>
                    <div class="value stage-badge-{DEPLOYMENT_STAGE}">{DEPLOYMENT_STAGE.upper()}</div>
                </div>
                <div class="info-card">
                    <h3>🎯 Status</h3>
                    <div class="value"><span class="status-indicator"></span>Running</div>
                </div>
            </div>

            <div class="actions">
                <a href="/health" class="btn">🔍 Health Check</a>
                <a href="/api/info" class="btn">📊 API Info</a>
            </div>

            <div class="footer">
                <p><strong>Purpose:</strong> Demonstrating Azure Container Apps blue-green deployments with Azure Developer CLI (azd)</p>
                <p>This app shows how different versions and revisions are displayed during blue-green deployments.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Container Apps."""
    uptime = int((datetime.now() - startup_time).total_seconds())
    
    return HealthResponse(
        status=f"healthy ({DEPLOYMENT_STAGE})",
        timestamp=datetime.now(),
        revision=REVISION_NAME,
        version=REVISION_COMMIT_ID,
        uptime_seconds=uptime
    )

@app.get("/api/info")
async def app_info():
    """Get application information."""
    return {
        "app_name": "Blue-Green Deployment Demo",
        "commit_id": REVISION_COMMIT_ID,
        "revision": REVISION_NAME,
        "deployment_stage": DEPLOYMENT_STAGE,
        "timestamp": datetime.now(),
        "environment": {
            "port": PORT,
            "python_version": "3.11+"
        }
    }

if __name__ == "__main__":
    logger.info(f"Starting Blue-Green Demo App (commit: {REVISION_COMMIT_ID}) on revision {REVISION_NAME}")
    logger.info(f"🌐 Open your browser and navigate to: http://localhost:{PORT}")
    logger.info(f"🔍 Health check available at: http://localhost:{PORT}/health")
    try:
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=PORT,
            log_level="info",
            reload=False
        )
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise