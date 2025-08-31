#!/usr/bin/env python3
"""
Enhanced AI Analysis Test for ChartAI Trading Assistant
Tests the improved trading suggestions and experience-level specific responses
"""

import requests
import json
import base64
import time
from datetime import datetime
from PIL import Image, ImageDraw
import io

# Configuration
BASE_URL = "https://trade-vision-7.preview.emergentagent.com/api"
TIMEOUT = 60  # Increased timeout for AI processing

class EnhancedAITester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message, response_data=None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        
    def create_realistic_chart_image(self):
        """Create a more realistic-looking chart image for testing"""
        # Create a 400x300 chart-like image
        img = Image.new('RGB', (400, 300), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw chart background
        draw.rectangle([50, 50, 350, 250], outline='black', width=2)
        
        # Draw some price lines to simulate a chart
        # Simulate an uptrend with some volatility
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
            height = 20 + (i % 40)  # Varying heights
            draw.rectangle([i, 250, i + 10, 250 + height], fill='gray')
        
        # Add grid lines
        for x in range(60, 340, 40):
            draw.line([(x, 50), (x, 250)], fill='lightgray', width=1)
        for y in range(70, 250, 30):
            draw.line([(50, y), (350, y)], fill='lightgray', width=1)
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return img_base64
        
    def test_enhanced_ai_analysis_by_level(self):
        """Test enhanced AI analysis for different experience levels"""
        test_image = self.create_realistic_chart_image()
        experience_levels = ["beginner", "intermediate", "advanced"]
        
        all_passed = True
        responses = {}
        
        for level in experience_levels:
            try:
                print(f"\n🔍 Testing {level.upper()} level analysis...")
                
                response = self.session.post(
                    f"{BASE_URL}/analyze-chart",
                    json={
                        "image_base64": test_image,
                        "experience_level": level
                    },
                    timeout=TIMEOUT
                )
                
                if response.status_code == 200:
                    data = response.json()
                    responses[level] = data
                    
                    # Test 1: Check all required fields are present
                    required_fields = [
                        "patterns_detected", "support_levels", "resistance_levels",
                        "trend_analysis", "trading_plan", "explanation", "experience_level"
                    ]
                    
                    missing_fields = [f for f in required_fields if f not in data]
                    if missing_fields:
                        self.log_test(f"Enhanced AI Analysis - {level} - Structure", 
                                    False, f"Missing fields: {missing_fields}")
                        all_passed = False
                        continue
                    
                    # Test 2: Check trading plan has specific fields
                    trading_plan = data.get("trading_plan", {})
                    tp_fields = ["entry_price", "exit_price", "stop_loss", "risk_reward_ratio"]
                    
                    missing_tp_fields = [f for f in tp_fields if f not in trading_plan]
                    if missing_tp_fields:
                        self.log_test(f"Enhanced AI Analysis - {level} - Trading Plan", 
                                    False, f"Missing trading plan fields: {missing_tp_fields}")
                        all_passed = False
                        continue
                    
                    # Test 3: Check for educational disclaimer
                    explanation = data.get("explanation", "").lower()
                    has_disclaimer = ("not financial advice" in explanation or 
                                    "educational purposes" in explanation)
                    
                    if not has_disclaimer:
                        self.log_test(f"Enhanced AI Analysis - {level} - Disclaimer", 
                                    False, "Missing educational disclaimer")
                        all_passed = False
                    else:
                        self.log_test(f"Enhanced AI Analysis - {level} - Disclaimer", 
                                    True, "Educational disclaimer present")
                    
                    # Test 4: Check for specific trading suggestions (not generic)
                    entry_price = trading_plan.get("entry_price", "")
                    exit_price = trading_plan.get("exit_price", "")
                    stop_loss = trading_plan.get("stop_loss", "")
                    risk_reward = trading_plan.get("risk_reward_ratio", "")
                    
                    # Check if AI provided specific analysis or generic responses
                    generic_responses = ["see explanation", "analysis completed", "n/a", "na", ""]
                    
                    specific_suggestions = True
                    generic_found = []
                    
                    for field_name, field_value in [
                        ("entry_price", entry_price), 
                        ("exit_price", exit_price),
                        ("stop_loss", stop_loss), 
                        ("risk_reward_ratio", risk_reward)
                    ]:
                        if any(generic in str(field_value).lower() for generic in generic_responses):
                            generic_found.append(field_name)
                            specific_suggestions = False
                    
                    if specific_suggestions:
                        self.log_test(f"Enhanced AI Analysis - {level} - Specific Suggestions", 
                                    True, "AI provided specific trading suggestions")
                    else:
                        self.log_test(f"Enhanced AI Analysis - {level} - Specific Suggestions", 
                                    False, f"Generic responses found in: {generic_found}")
                        all_passed = False
                    
                    # Test 5: Check trend analysis is not empty
                    trend_analysis = data.get("trend_analysis", "").strip()
                    if len(trend_analysis) > 10:  # Should have meaningful content
                        self.log_test(f"Enhanced AI Analysis - {level} - Trend Analysis", 
                                    True, f"Comprehensive trend analysis provided ({len(trend_analysis)} chars)")
                    else:
                        self.log_test(f"Enhanced AI Analysis - {level} - Trend Analysis", 
                                    False, "Trend analysis too brief or empty")
                        all_passed = False
                    
                    # Test 6: Check patterns detected
                    patterns = data.get("patterns_detected", [])
                    if isinstance(patterns, list) and len(patterns) > 0:
                        self.log_test(f"Enhanced AI Analysis - {level} - Patterns", 
                                    True, f"Detected {len(patterns)} patterns: {patterns[:2]}")
                    else:
                        self.log_test(f"Enhanced AI Analysis - {level} - Patterns", 
                                    False, "No patterns detected or invalid format")
                        all_passed = False
                    
                    print(f"   📊 Patterns: {patterns[:2] if patterns else 'None'}")
                    print(f"   📈 Entry: {entry_price}")
                    print(f"   📉 Exit: {exit_price}")
                    print(f"   🛑 Stop Loss: {stop_loss}")
                    print(f"   ⚖️ Risk/Reward: {risk_reward}")
                    
                else:
                    self.log_test(f"Enhanced AI Analysis - {level}", 
                                False, f"HTTP {response.status_code}: {response.text}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Enhanced AI Analysis - {level}", 
                            False, f"Request error: {str(e)}")
                all_passed = False
        
        # Test 7: Compare responses between experience levels
        if len(responses) == 3:
            self.compare_experience_levels(responses)
        
        return all_passed
    
    def compare_experience_levels(self, responses):
        """Compare AI responses between different experience levels"""
        try:
            beginner_exp = responses["beginner"]["explanation"]
            intermediate_exp = responses["intermediate"]["explanation"]
            advanced_exp = responses["advanced"]["explanation"]
            
            # Check if explanations are different (indicating level-specific responses)
            if (beginner_exp != intermediate_exp and 
                intermediate_exp != advanced_exp and 
                beginner_exp != advanced_exp):
                self.log_test("Experience Level Differentiation", 
                            True, "AI provides different explanations for each experience level")
            else:
                self.log_test("Experience Level Differentiation", 
                            False, "AI responses are too similar across experience levels")
            
            # Check explanation complexity (advanced should be longer/more detailed)
            lengths = {
                "beginner": len(beginner_exp),
                "intermediate": len(intermediate_exp), 
                "advanced": len(advanced_exp)
            }
            
            print(f"   📝 Explanation lengths - Beginner: {lengths['beginner']}, "
                  f"Intermediate: {lengths['intermediate']}, Advanced: {lengths['advanced']}")
            
            if lengths["advanced"] >= lengths["intermediate"] >= lengths["beginner"]:
                self.log_test("Experience Level Complexity", 
                            True, "Advanced explanations are more detailed than beginner")
            else:
                self.log_test("Experience Level Complexity", 
                            False, "Explanation complexity doesn't match experience levels")
                
        except Exception as e:
            self.log_test("Experience Level Comparison", 
                        False, f"Error comparing levels: {str(e)}")
    
    def test_error_handling_enhanced(self):
        """Test enhanced error handling scenarios"""
        all_passed = True
        
        # Test with invalid experience level
        try:
            test_image = self.create_realistic_chart_image()
            response = self.session.post(
                f"{BASE_URL}/analyze-chart",
                json={
                    "image_base64": test_image,
                    "experience_level": "expert"  # Invalid level
                },
                timeout=TIMEOUT
            )
            
            # Should either accept it or reject it gracefully
            if response.status_code in [200, 400, 422]:
                self.log_test("Error Handling - Invalid Experience Level", 
                            True, f"Handled invalid experience level appropriately: {response.status_code}")
            else:
                self.log_test("Error Handling - Invalid Experience Level", 
                            False, f"Unexpected response: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Error Handling - Invalid Experience Level", 
                        False, f"Request error: {str(e)}")
            all_passed = False
        
        # Test with empty image
        try:
            response = self.session.post(
                f"{BASE_URL}/analyze-chart",
                json={
                    "image_base64": "",
                    "experience_level": "beginner"
                },
                timeout=TIMEOUT
            )
            
            if response.status_code in [400, 422]:
                self.log_test("Error Handling - Empty Image", 
                            True, f"Correctly rejected empty image: {response.status_code}")
            else:
                self.log_test("Error Handling - Empty Image", 
                            False, f"Should reject empty image: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Error Handling - Empty Image", 
                        False, f"Request error: {str(e)}")
            all_passed = False
        
        return all_passed
    
    def run_enhanced_tests(self):
        """Run all enhanced AI analysis tests"""
        print("=" * 70)
        print("ChartAI Enhanced AI Analysis Test Suite")
        print("=" * 70)
        print(f"Testing against: {BASE_URL}")
        print(f"Started at: {datetime.now().isoformat()}")
        print()
        
        tests = [
            ("Enhanced AI Analysis by Experience Level", self.test_enhanced_ai_analysis_by_level),
            ("Enhanced Error Handling", self.test_error_handling_enhanced)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n--- Running {test_name} Tests ---")
            if test_func():
                passed += 1
        
        # Summary
        print("\n" + "=" * 70)
        print("ENHANCED AI TEST SUMMARY")
        print("=" * 70)
        print(f"Total Test Categories: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Detailed results
        print("\nDETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
        
        return passed == total

if __name__ == "__main__":
    tester = EnhancedAITester()
    success = tester.run_enhanced_tests()
    
    if success:
        print("\n🎉 All enhanced AI tests passed! The enhanced analysis system is working correctly.")
        exit(0)
    else:
        print("\n⚠️  Some enhanced AI tests failed. Check the results above.")
        exit(1)