#!/usr/bin/env python3
"""
Debug AI Response - Check what the AI is actually returning
"""

import requests
import json
import base64
from PIL import Image, ImageDraw
import io

BASE_URL = "https://trade-vision-7.preview.emergentagent.com/api"

def create_realistic_chart_image():
    """Create a more realistic-looking chart image for testing"""
    img = Image.new('RGB', (400, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw chart background
    draw.rectangle([50, 50, 350, 250], outline='black', width=2)
    
    # Draw some price lines to simulate a chart
    points = [
        (60, 200), (80, 190), (100, 195), (120, 180), (140, 175),
        (160, 170), (180, 165), (200, 160), (220, 155), (240, 150),
        (260, 145), (280, 140), (300, 135), (320, 130), (340, 125)
    ]
    
    # Draw the price line
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill='blue', width=2)
    
    # Add some volume bars at the bottom
    for i in range(60, 340, 20):
        height = 20 + (i % 40)
        draw.rectangle([i, 250, i + 10, 250 + height], fill='gray')
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_base64

def test_ai_response():
    """Test and debug AI response"""
    test_image = create_realistic_chart_image()
    
    response = requests.post(
        f"{BASE_URL}/analyze-chart",
        json={
            "image_base64": test_image,
            "experience_level": "advanced"
        },
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        print("=== AI RESPONSE DEBUG ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response Keys: {list(data.keys())}")
        print()
        
        print("PATTERNS DETECTED:")
        print(json.dumps(data.get("patterns_detected", []), indent=2))
        print()
        
        print("SUPPORT LEVELS:")
        print(json.dumps(data.get("support_levels", []), indent=2))
        print()
        
        print("RESISTANCE LEVELS:")
        print(json.dumps(data.get("resistance_levels", []), indent=2))
        print()
        
        print("TREND ANALYSIS:")
        print(data.get("trend_analysis", ""))
        print()
        
        print("TRADING PLAN:")
        trading_plan = data.get("trading_plan", {})
        print(json.dumps(trading_plan, indent=2))
        print()
        
        print("EXPLANATION (first 500 chars):")
        explanation = data.get("explanation", "")
        print(explanation[:500] + "..." if len(explanation) > 500 else explanation)
        print()
        
        print("EXPERIENCE LEVEL:")
        print(data.get("experience_level", ""))
        
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_ai_response()