# ChartAI – Smart Trading Assistant 📈

A mobile application that uses AI to analyze financial charts and provide educational trading insights for stocks, crypto, forex, and other markets.

## 🎯 Purpose

ChartAI allows users to upload financial charts and receive AI-powered analysis including:
- Pattern detection and recognition
- Support and resistance level identification  
- Trend analysis and market insights
- Personalized trading plans with entry/exit/stop-loss recommendations
- Risk/reward ratio calculations
- Educational explanations tailored to user experience level

⚠️ **Important**: All analysis is for educational purposes only and is not financial advice.

## ✨ Core Features (MVP)

### 1. 📷 Image Upload & Camera
- Take photos of charts directly with camera
- Upload existing chart images from gallery  
- Support for all major chart types (stocks, crypto, forex, futures)
- Image quality validation and processing

### 2. 🧠 AI-Powered Analysis
- Advanced pattern recognition using GPT-4o Vision
- Intelligent support and resistance level detection
- Comprehensive trend analysis
- Market structure evaluation
- Volume and price action analysis

### 3. 📊 Personalized Trading Plans
- **Entry Price**: Optimal entry points with confirmation signals
- **Exit Price**: Target prices based on technical analysis
- **Stop Loss**: Risk management levels with reasoning
- **Risk/Reward Ratio**: Calculated ratios with explanations

### 4. 👥 Experience-Based Explanations
- **Beginner**: Simple explanations, basic concepts, clear guidance
- **Intermediate**: Moderate complexity, technical analysis terms
- **Advanced**: Comprehensive analysis, professional terminology

### 5. 📱 Enhanced Results Display
- Interactive chart visualizations
- Risk/reward pie charts
- Support/resistance bar charts
- Tabular data presentation
- Detailed explanations with educational context

## 🏗️ Technical Architecture

### Frontend (React Native/Expo)
- **Platform**: iOS and Android compatible
- **Framework**: React Native with Expo
- **Navigation**: Expo Router
- **Charts**: React Native Chart Kit with SVG
- **Storage**: AsyncStorage for user preferences
- **Camera**: Expo ImagePicker for photo capture

### Backend (FastAPI)
- **Framework**: FastAPI with Python
- **Database**: MongoDB with Motor async driver
- **AI Integration**: GPT-4o Vision via Emergent LLM API
- **Image Processing**: Pillow for image handling
- **API**: RESTful endpoints with JSON responses

## 📁 Project Structure

```
ChartAI/
├── frontend/                 # React Native mobile app
│   ├── app/                 # Screen components
│   │   ├── index.tsx        # Onboarding/experience selection
│   │   ├── upload.tsx       # Chart upload and camera
│   │   ├── results.tsx      # Analysis results with charts
│   │   └── settings.tsx     # User settings and preferences
│   ├── assets/              # Images and static files
│   └── package.json         # Dependencies and scripts
├── backend/                 # FastAPI server
│   ├── server.py           # Main API server
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment configuration
├── test_chartai.py         # Automated testing framework
├── MANUAL_TESTING_CHECKLIST.md  # Manual testing guide
└── README.md              # This file
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.9+
- MongoDB instance
- Emergent LLM API key

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### Environment Configuration
Create `.env` files in both frontend and backend directories:

**Backend `.env`:**
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=chartai_db
EMERGENT_LLM_KEY=your_api_key_here
```

**Frontend `.env`:**
```
EXPO_PUBLIC_BACKEND_URL=http://localhost:8000
```

## 🧪 Testing

### Automated Testing
Run the automated test suite:
```bash
python test_chartai.py
```

Tests include:
- Backend health checks
- API endpoint validation
- Chart analysis functionality
- Experience level differentiation
- Financial disclaimer compliance

### Manual Testing
Follow the comprehensive manual testing checklist in `MANUAL_TESTING_CHECKLIST.md` covering:
- User interface testing
- AI analysis quality
- Cross-platform compatibility
- Error handling
- Performance validation

## 📱 User Experience Flow

1. **Onboarding**: User selects experience level (Beginner/Intermediate/Advanced)
2. **Upload**: User captures or selects a chart image
3. **Analysis**: AI processes the chart and generates insights
4. **Results**: User views comprehensive analysis with visualizations
5. **Action**: User can analyze another chart or adjust settings

## 🛡️ Legal & Compliance

- Prominent financial disclaimers on every screen
- "Not financial advice" warnings in all analysis
- "Educational purposes only" clearly stated
- Age-appropriate content and legal compliance
- Privacy-focused design with minimal data collection

## 🔧 API Endpoints

### Core Endpoints
- `GET /api/health` - Health check
- `POST /api/user-preferences` - Save user experience level
- `POST /api/analyze-chart` - Analyze uploaded chart
- `GET /api/status` - System status check

### Request/Response Examples

**Chart Analysis Request:**
```json
{
  "image_base64": "base64_encoded_image_data",
  "experience_level": "intermediate"
}
```

**Chart Analysis Response:**
```json
{
  "id": "uuid",
  "patterns_detected": ["Ascending Triangle", "Support Break"],
  "support_levels": ["$45.20 - Previous low", "$44.85 - Volume support"],
  "resistance_levels": ["$47.50 - Previous high", "$48.00 - Psychological level"],
  "trend_analysis": "Bullish trend with strong momentum...",
  "trading_plan": {
    "entry_price": "$46.20 - Break above resistance",
    "exit_price": "$49.00 - Target based on pattern height",
    "stop_loss": "$44.50 - Below support level",
    "risk_reward_ratio": "1:2.1 - Good risk/reward setup"
  },
  "explanation": "Detailed educational explanation...",
  "experience_level": "intermediate",
  "created_at": "2024-01-01T12:00:00Z"
}
```

## 🎨 UI/UX Features

### Visual Design
- Modern dark theme with professional colors
- Consistent iconography and branding
- Responsive layout for different screen sizes
- Smooth animations and transitions

### Chart Visualizations
- Risk/reward pie charts
- Support/resistance bar charts
- Pattern confidence indicators
- Interactive data displays

### User-Friendly Elements
- Clear navigation with breadcrumbs
- Loading states with progress indicators
- Error handling with helpful messages
- Accessibility features for all users

## 🔮 Future Enhancements (Post-MVP)

- Premium subscription features
- User authentication and cloud sync
- Historical analysis tracking
- PDF export functionality
- Social sharing capabilities
- Advanced chart drawing tools
- Real-time market data integration
- Portfolio tracking features

## 🤝 Contributing

This is a private project. For development:
1. Follow the existing code style and patterns
2. Add tests for new features
3. Update documentation as needed
4. Ensure all disclaimers remain intact

## 📄 License

Private project. All rights reserved.

## 📞 Support

For technical issues or questions about the ChartAI app, please refer to the testing documentation and ensure all prerequisites are met.

---

**Disclaimer**: ChartAI is an educational tool designed to help users learn about technical analysis. All analysis provided is for educational purposes only and should not be considered as financial advice. Users should conduct their own research and consider their financial situation before making any investment decisions.