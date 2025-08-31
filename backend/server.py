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
from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

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

# Helper function to get AI analysis
async def analyze_chart_with_ai(image_base64: str, experience_level: str) -> ChartAnalysisResult:
    try:
        # Initialize LLM chat
        api_key = os.getenv("EMERGENT_LLM_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="AI service not configured")
        
        session_id = str(uuid.uuid4())
        
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
        
        chat = LlmChat(
            api_key=api_key,
            session_id=session_id,
            system_message=system_message
        ).with_model("openai", "gpt-4o")
        
        # Create image content
        image_content = ImageContent(image_base64=image_base64)
        
        # Create detailed analysis prompt based on experience level
        base_prompt = """You are analyzing a financial trading chart. Please provide a comprehensive technical analysis with specific, actionable trading suggestions.

IMPORTANT: Always examine the chart carefully for:
- Current price levels and recent price action
- Key support and resistance zones
- Volume patterns (if visible)
- Trend direction and momentum
- Chart patterns and formations
- Entry and exit opportunities

Provide specific price levels based on what you can observe in the chart, not generic responses."""

        if experience_level == "beginner":
            analysis_prompt = f"""{base_prompt}

For a BEGINNER trader, analyze this chart and provide:

1. **Patterns Detected**: Identify simple, clear chart patterns (e.g., "Ascending Triangle", "Double Bottom", "Support/Resistance Break")
2. **Support Levels**: List 2-3 key price levels where the chart has bounced up from (be specific: e.g., "$45.20", "$44.85")
3. **Resistance Levels**: List 2-3 key price levels where price has been rejected (be specific with prices)
4. **Trend Analysis**: Simple trend direction with easy-to-understand reasoning (bullish/bearish/sideways)
5. **Trading Plan**: Provide specific actionable levels:
   - Entry Price: Optimal entry point based on chart analysis
   - Exit Price: First profit target based on technical levels
   - Stop Loss: Risk management level to limit losses
   - Risk/Reward Ratio: Calculate and explain (e.g., "1:2" means risk $1 to make $2)
6. **Explanation**: Simple, educational explanation focusing on basic concepts

Use simple language and explain WHY each level is important. Always end with: "This is not financial advice. This analysis is for educational purposes only."

Format as JSON:"""
        elif experience_level == "intermediate":
            analysis_prompt = f"""{base_prompt}

For an INTERMEDIATE trader, analyze this chart and provide:

1. **Patterns Detected**: Identify chart patterns with confluence factors (e.g., "Bullish Flag with Volume Confirmation", "Head and Shoulders with RSI Divergence")
2. **Support Levels**: Identify 3-4 key support zones with historical significance and volume analysis
3. **Resistance Levels**: Identify 3-4 resistance levels including psychological levels and previous highs/lows
4. **Trend Analysis**: Multi-timeframe trend analysis with momentum assessment and potential reversals
5. **Trading Plan**: Detailed trading strategy:
   - Entry Price: Optimal entry with confirmation signals required
   - Exit Price: Multiple profit targets (PT1, PT2) based on Fibonacci or measured moves
   - Stop Loss: Calculated based on technical levels and volatility
   - Risk/Reward Ratio: Precise calculation with position sizing considerations
6. **Explanation**: Technical analysis with moderate complexity, including multiple timeframe context

Include confluence factors and explain the reasoning behind each level. Always end with: "This is not financial advice. This analysis is for educational purposes only."

Format as JSON:"""
        else:  # advanced
            analysis_prompt = f"""{base_prompt}

For an ADVANCED trader, analyze this chart and provide:

1. **Patterns Detected**: Comprehensive pattern analysis including complex formations, Elliott Wave patterns, and institutional levels
2. **Support Levels**: Dynamic and static support levels with volume profile analysis, order flow, and market structure
3. **Resistance Levels**: Multi-layered resistance analysis including supply zones, liquidity levels, and algorithmic levels
4. **Trend Analysis**: Advanced trend analysis with market structure, momentum divergences, sector rotation, and macro factors
5. **Trading Plan**: Professional trading strategy:
   - Entry Price: Precise entry with multiple confirmation signals and risk parameters
   - Exit Price: Scaled exit strategy with multiple targets based on advanced technical analysis
   - Stop Loss: Dynamic stop-loss strategy considering volatility, market conditions, and position management
   - Risk/Reward Ratio: Advanced risk management with portfolio correlation and Kelly Criterion considerations
6. **Explanation**: Comprehensive analysis suitable for professional traders, including market microstructure and advanced concepts

Provide institutional-level analysis with specific price levels, volume analysis, and market structure. Always end with: "This is not financial advice. This analysis is for educational purposes only."

Format as JSON:"""

        analysis_prompt += """
{
  "patterns_detected": ["specific pattern names with details"],
  "support_levels": ["$XX.XX - reason for this level", "$XX.XX - reason for this level"],
  "resistance_levels": ["$XX.XX - reason for this level", "$XX.XX - reason for this level"],
  "trend_analysis": "comprehensive trend analysis with specific reasoning",
  "trading_plan": {
    "entry_price": "$XX.XX - specific entry reason and confirmation needed",
    "exit_price": "$XX.XX - target based on technical analysis (or multiple targets PT1: $XX.XX, PT2: $XX.XX)",
    "stop_loss": "$XX.XX - risk management level with specific reasoning",
    "risk_reward_ratio": "1:X ratio with calculation explanation"
  },
  "explanation": "detailed technical analysis explanation with educational disclaimer"
}

CRITICAL: Provide actual price levels based on what you observe in the chart. If you cannot clearly see price levels, state that clearly but still provide analysis based on relative levels and patterns visible."""
        
        # Send message with image
        user_message = UserMessage(
            text=analysis_prompt,
            file_contents=[image_content]
        )
        
        response = await chat.send_message(user_message)
        
        # Parse the response (assuming it's JSON format)
        import json
        import re
        try:
            # First try to parse as direct JSON
            analysis_data = json.loads(response)
        except json.JSONDecodeError:
            try:
                # Try to extract JSON from markdown code blocks
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    analysis_data = json.loads(json_str)
                else:
                    # Try to find any JSON-like structure in the response
                    json_match = re.search(r'(\{.*?\})', response, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1)
                        analysis_data = json.loads(json_str)
                    else:
                        raise json.JSONDecodeError("No JSON found", response, 0)
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
                    "explanation": response
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
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# API Routes
@api_router.get("/")
async def root():
    return {"message": "ChartAI Trading Assistant API"}

@api_router.post("/user-preferences", response_model=UserPreferences)
async def save_user_preferences(preferences: UserPreferencesCreate):
    """Save user experience level preferences"""
    prefs_dict = preferences.dict()
    prefs_obj = UserPreferences(**prefs_dict)
    await db.user_preferences.insert_one(prefs_obj.dict())
    return prefs_obj

@api_router.get("/user-preferences")
async def get_user_preferences():
    """Get the latest user preferences"""
    prefs = await db.user_preferences.find().sort("created_at", -1).limit(1).to_list(1)
    if prefs:
        return UserPreferences(**prefs[0])
    return {"experience_level": "beginner"}

@api_router.post("/analyze-chart", response_model=ChartAnalysisResult)
async def analyze_chart(request: ChartAnalysisRequest):
    """Analyze a financial chart image"""
    try:
        # Validate base64 image
        if not request.image_base64:
            raise HTTPException(status_code=400, detail="No image provided")
        
        # Perform AI analysis
        result = await analyze_chart_with_ai(request.image_base64, request.experience_level)
        
        # Save to database
        await db.chart_analyses.insert_one(result.dict())
        
        return result
        
    except Exception as e:
        logging.error(f"Chart analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analysis-history", response_model=List[ChartAnalysisResult])
async def get_analysis_history():
    """Get recent chart analysis history"""
    analyses = await db.chart_analyses.find().sort("created_at", -1).limit(10).to_list(10)
    return [ChartAnalysisResult(**analysis) for analysis in analyses]

# Original status endpoints
@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()