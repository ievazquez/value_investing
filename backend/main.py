"""
Value Investing Analyzer - Backend API
FastAPI application for analyzing stocks using value investing principles
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import stock_routes
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Value Investing Analyzer API",
    description="API for analyzing stocks using Benjamin Graham and Warren Buffett principles",
    version="1.0.0"
)

# Configure CORS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stock_routes.router, prefix="/api", tags=["stocks"])

@app.get("/")
def read_root():
    return {
        "message": "Value Investing Analyzer API",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=True)
