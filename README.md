# MarketMind AI Platform

**MarketMind** is a Generative AI-Powered Sales & Marketing Intelligence Platform. It features intelligent services for creating marketing campaigns, sales pitches, and lead scoring, all backed by **Explainable AI (XAI)** to provide transparent reasoning for every generated output.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- API Keys for Groq/Gemini (Optional for Demo Mode)

### Running the Application (One-Click)
Simply run the `start_app.bat` script in the root directory.
```bash
./start_app.bat
```

### Manual Startup

**1. Backend (FastAPI)**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**2. Frontend (React)**
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Accessing the App
Open your browser and navigate to:
**http://localhost:5173**

## ✨ Features
- **Campaign Generator**: Create platform-specific social media posts with AI reasoning.
- **Sales Pitch Generator**: Generate personalized pitches.
- **Lead Scoring**: AI-driven lead qualification.

## 🔑 Configuration
Create a `.env` file in the `backend` directory:
```
GROQ_API_KEY=your_key_here
```
*Note: If no key is provided, the app runs in "Demo Mode" with mock data.*
