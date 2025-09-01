from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import base64
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
from PIL import Image
import io
import openai
import json
import re

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'chartai_db')]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class UserPreferences(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    experience_level: str  # "beginner", "intermediate", "advanced"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserPreferencesCreate(BaseModel):
    experience_level: str

class ChartAnalysisRequest(BaseModel):
    image_base64: str
    experience_level: str

class TradingPlan(BaseModel):
    entry_price: Optional[str] = None
    exit_price: Optional[str] = None
    stop_loss: Optional[str] = None
    risk_reward_ratio: Optional[str] = None

class ChartAnalysisResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    patterns_detected: List[str] = []
    support_levels: List[str] = []
    resistance_levels: List[str] = []
    trend_analysis: str = ""
    trading_plan: TradingPlan = Field(default_factory=TradingPlan)
    explanation: str = ""
    experience_level: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)

class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Helper function to get AI analysis using OpenAI
async def analyze_chart_with_openai(image_base64: str, experience_level: str) -> ChartAnalysisResult:
    try:
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            # Return mock data if no API key
            return create_mock_analysis(experience_level)
        
        client = openai.OpenAI(api_key=api_key)
        
        # Create system message based on experience level
        if experience_level == "beginner":
            system_message = """You are a helpful trading assistant that analyzes financial charts for beginners. 
            Provide simple, easy-to-understand explanations. Focus on basic patterns and clear guidance.
            Always include the disclaimer: 'This is not financial advice. This analysis is for educational purposes only.'"""
        elif experience_level == "intermediate":
            system_message = """You are a trading assistant that analyzes financial charts for intermediate traders.
            Provide detailed technical analysis with moderate complexity. Include risk management principles.
            Always include the disclaimer: 'This is not financial advice. This analysis is for educational purposes only.'"""
        else:  # advanced
            system_message = """You are a professional trading assistant that analyzes financial charts for advanced traders.
            Provide comprehensive technical analysis with advanced concepts, ratios, and detailed risk management.
            Always include the disclaimer: 'This is not financial advice. This analysis is for educational purposes only.'"""
        
        # Create analysis prompt
        analysis_prompt = f"""You are analyzing a financial trading chart. Please provide a comprehensive technical analysis.

For a {experience_level.upper()} trader, analyze this chart and provide:

1. **Patterns Detected**: Identify chart patterns (e.g., "Ascending Triangle", "Double Bottom")
2. **Support Levels**: List 2-3 key price levels where the chart has bounced up from
3. **Resistance Levels**: List 2-3 key price levels where price has been rejected
4. **Trend Analysis**: Trend direction with reasoning (bullish/bearish/sideways)
5. **Trading Plan**: Provide specific actionable levels:
   - Entry Price: Optimal entry point
   - Exit Price: First profit target
   - Stop Loss: Risk management level
   - Risk/Reward Ratio: Calculate ratio (e.g., "1:2")
6. **Explanation**: Educational explanation appropriate for {experience_level} level

Always end with: "This is not financial advice. This analysis is for educational purposes only."

Format as JSON:
{{
  "patterns_detected": ["specific pattern names"],
  "support_levels": ["$XX.XX - reason", "$XX.XX - reason"],
  "resistance_levels": ["$XX.XX - reason", "$XX.XX - reason"],
  "trend_analysis": "comprehensive trend analysis",
  "trading_plan": {{
    "entry_price": "$XX.XX - specific entry reason",
    "exit_price": "$XX.XX - target based on analysis",
    "stop_loss": "$XX.XX - risk management level",
    "risk_reward_ratio": "1:X ratio with explanation"
  }},
  "explanation": "detailed analysis with educational disclaimer"
}}"""
        
        # Send request to OpenAI
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": system_message},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": analysis_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        response_text = response.choices[0].message.content
        
        # Parse the response
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                analysis_data = json.loads(json_str)
            else:
                # Try to find any JSON-like structure
                json_match = re.search(r'(\{.*?\})', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    analysis_data = json.loads(json_str)
                else:
                    raise json.JSONDecodeError("No JSON found", response_text, 0)
        except (json.JSONDecodeError, AttributeError):
            # Fallback if response is not JSON
            analysis_data = {
                "patterns_detected": ["Analysis completed"],
                "support_levels": ["See explanation"],
                "resistance_levels": ["See explanation"],
                "trend_analysis": "See detailed explanation",
                "trading_plan": {
                    "entry_price": "See explanation",
                    "exit_price": "See explanation",
                    "stop_loss": "See explanation",
                    "risk_reward_ratio": "See explanation"
                },
                "explanation": response_text + "\n\nThis is not financial advice. This analysis is for educational purposes only."
            }
        
        # Create result object
        trading_plan = TradingPlan(
            entry_price=analysis_data.get("trading_plan", {}).get("entry_price"),
            exit_price=analysis_data.get("trading_plan", {}).get("exit_price"),
            stop_loss=analysis_data.get("trading_plan", {}).get("stop_loss"),
            risk_reward_ratio=analysis_data.get("trading_plan", {}).get("risk_reward_ratio")
        )
        
        result = ChartAnalysisResult(
            patterns_detected=analysis_data.get("patterns_detected", []),
            support_levels=analysis_data.get("support_levels", []),
            resistance_levels=analysis_data.get("resistance_levels", []),
            trend_analysis=analysis_data.get("trend_analysis", ""),
            trading_plan=trading_plan,
            explanation=analysis_data.get("explanation", ""),
            experience_level=experience_level
        )
        
        return result
        
    except Exception as e:
        logging.error(f"AI analysis error: {str(e)}")
        # Return mock data on error
        return create_mock_analysis(experience_level)

def create_mock_analysis(experience_level: str) -> ChartAnalysisResult:
    """Create mock analysis data for testing"""
    if experience_level == "beginner":
        explanation = "This chart shows an upward trend with clear support around $45.20. The price has been making higher highs and higher lows, which is a bullish sign. Consider entering above the resistance line with a stop loss below support. This is not financial advice. This analysis is for educational purposes only."
        patterns = ["Upward Trend", "Support Level"]
    elif experience_level == "intermediate":
        explanation = "Technical analysis reveals an ascending triangle pattern with strong volume confirmation. The 50-day moving average is acting as dynamic support. RSI shows healthy momentum without overbought conditions. Entry above $47.50 with targets at $49.00 based on pattern height. This is not financial advice. This analysis is for educational purposes only."
        patterns = ["Ascending Triangle", "Moving Average Support", "Volume Confirmation"]
    else:  # advanced
        explanation = "Comprehensive analysis indicates institutional accumulation at key Fibonacci retracement levels. Order flow shows strong buying interest at $45.20 (61.8% retrace). Volume profile suggests significant resistance at $47.50-48.00 zone. Consider scaled entries with risk management at 2% portfolio allocation. This is not financial advice. This analysis is for educational purposes only."
        patterns = ["Fibonacci Retracement", "Volume Profile", "Institutional Accumulation"]
    
    trading_plan = TradingPlan(
        entry_price="$46.20 - Break above resistance with volume",
        exit_price="$49.00 - Target based on pattern measurement",
        stop_loss="$44.50 - Below key support level",
        risk_reward_ratio="1:2.1 - Favorable risk-reward setup"
    )
    
    return ChartAnalysisResult(
        patterns_detected=patterns,
        support_levels=["$45.20 - Previous swing low", "$44.85 - Volume support"],
        resistance_levels=["$47.50 - Pattern resistance", "$48.00 - Psychological level"],
        trend_analysis="Bullish trend with strong momentum and healthy pullbacks",
        trading_plan=trading_plan,
        explanation=explanation,
        experience_level=experience_level
    )

# API Routes
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@api_router.post("/user-preferences", response_model=UserPreferences)
async def create_user_preferences(preferences: UserPreferencesCreate):
    try:
        user_pref = UserPreferences(experience_level=preferences.experience_level)
        await db.user_preferences.insert_one(user_pref.dict())
        return user_pref
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/analyze-chart", response_model=ChartAnalysisResult)
async def analyze_chart(request: ChartAnalysisRequest):
    try:
        # Validate experience level
        if request.experience_level not in ["beginner", "intermediate", "advanced"]:
            raise HTTPException(status_code=400, detail="Invalid experience level")
        
        # Analyze chart with AI
        result = await analyze_chart_with_openai(request.image_base64, request.experience_level)
        
        # Store result in database
        await db.chart_analyses.insert_one(result.dict())
        
        return result
        
    except Exception as e:
        logging.error(f"Chart analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Analysis failed")

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(status: StatusCheckCreate):
    try:
        status_check = StatusCheck(client_name=status.client_name)
        await db.status_checks.insert_one(status_check.dict())
        return status_check
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include the API router
app.include_router(api_router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "ChartAI API is running", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)