from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="MarketMind API",
    description="Generative AI-Powered Sales & Marketing Intelligence Platform with Explainable AI",
    version="1.0.0"
)

# CORS Middleware to allow requests from Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "MarketMind API is running",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

from app.routers import campaign, pitch, lead
app.include_router(campaign.router)
app.include_router(pitch.router)
app.include_router(lead.router)
