#!/usr/bin/env python3
"""
ChartAI Trading Assistant Backend Test Suite
Tests all API endpoints and core functionality
"""

import requests
import json
import base64
import time
from datetime import datetime
from PIL import Image
import io

# Configuration
BASE_URL = "https://trade-vision-7.preview.emergentagent.com/api"
TIMEOUT = 30

class ChartAITester:
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
        
    def create_test_image_base64(self):
        """Create a simple test chart image as base64"""
        # Create a simple test image (100x100 white square with some lines)
        img = Image.new('RGB', (100, 100), color='white')
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return img_base64
        
    def test_root_endpoint(self):
        """Test GET /api/ - Root endpoint check"""
        try:
            response = self.session.get(f"{BASE_URL}/", timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "ChartAI" in data["message"]:
                    self.log_test("Root Endpoint", True, "Root endpoint responding correctly", data)
                    return True
                else:
                    self.log_test("Root Endpoint", False, f"Unexpected response format: {data}")
                    return False
            else:
                self.log_test("Root Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Connection error: {str(e)}")
            return False
            
    def test_save_user_preferences(self):
        """Test POST /api/user-preferences - Save user experience level"""
        test_cases = [
            {"experience_level": "beginner"},
            {"experience_level": "intermediate"}, 
            {"experience_level": "advanced"}
        ]
        
        all_passed = True
        
        for i, test_data in enumerate(test_cases):
            try:
                response = self.session.post(
                    f"{BASE_URL}/user-preferences",
                    json=test_data,
                    timeout=TIMEOUT
                )
                
                if response.status_code == 200:
                    data = response.json()
                    required_fields = ["id", "experience_level", "created_at"]
                    
                    if all(field in data for field in required_fields):
                        if data["experience_level"] == test_data["experience_level"]:
                            self.log_test(f"Save User Preferences ({test_data['experience_level']})", 
                                        True, "Preferences saved successfully", data)
                        else:
                            self.log_test(f"Save User Preferences ({test_data['experience_level']})", 
                                        False, f"Experience level mismatch: expected {test_data['experience_level']}, got {data['experience_level']}")
                            all_passed = False
                    else:
                        missing_fields = [f for f in required_fields if f not in data]
                        self.log_test(f"Save User Preferences ({test_data['experience_level']})", 
                                    False, f"Missing required fields: {missing_fields}")
                        all_passed = False
                else:
                    self.log_test(f"Save User Preferences ({test_data['experience_level']})", 
                                False, f"HTTP {response.status_code}: {response.text}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Save User Preferences ({test_data['experience_level']})", 
                            False, f"Request error: {str(e)}")
                all_passed = False
                
        return all_passed
        
    def test_get_user_preferences(self):
        """Test GET /api/user-preferences - Get current user preferences"""
        try:
            response = self.session.get(f"{BASE_URL}/user-preferences", timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                
                # Should have experience_level at minimum
                if "experience_level" in data:
                    valid_levels = ["beginner", "intermediate", "advanced"]
                    if data["experience_level"] in valid_levels:
                        self.log_test("Get User Preferences", True, 
                                    f"Retrieved preferences: {data['experience_level']}", data)
                        return True
                    else:
                        self.log_test("Get User Preferences", False, 
                                    f"Invalid experience level: {data['experience_level']}")
                        return False
                else:
                    self.log_test("Get User Preferences", False, 
                                "Missing experience_level in response")
                    return False
            else:
                self.log_test("Get User Preferences", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Get User Preferences", False, f"Request error: {str(e)}")
            return False
            
    def test_chart_analysis(self):
        """Test POST /api/analyze-chart - Main chart analysis endpoint"""
        # Create test image
        test_image_base64 = self.create_test_image_base64()
        
        test_cases = [
            {"image_base64": test_image_base64, "experience_level": "beginner"},
            {"image_base64": test_image_base64, "experience_level": "intermediate"},
            {"image_base64": test_image_base64, "experience_level": "advanced"}
        ]
        
        all_passed = True
        
        for test_data in test_cases:
            try:
                response = self.session.post(
                    f"{BASE_URL}/analyze-chart",
                    json=test_data,
                    timeout=TIMEOUT
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check required response fields
                    required_fields = [
                        "id", "patterns_detected", "support_levels", 
                        "resistance_levels", "trend_analysis", "trading_plan", 
                        "explanation", "experience_level", "created_at"
                    ]
                    
                    missing_fields = [f for f in required_fields if f not in data]
                    if not missing_fields:
                        # Check trading_plan structure
                        trading_plan = data.get("trading_plan", {})
                        trading_plan_fields = ["entry_price", "exit_price", "stop_loss", "risk_reward_ratio"]
                        
                        if all(field in trading_plan for field in trading_plan_fields):
                            # Check response - if AI can't process image, that's expected for test image
                            explanation = data.get("explanation", "")
                            if ("unable to view" in explanation.lower() or 
                                "can't analyze" in explanation.lower() or
                                "cannot analyze" in explanation.lower()):
                                self.log_test(f"Chart Analysis ({test_data['experience_level']})", 
                                            True, "AI correctly identified invalid test image - backend working", 
                                            {k: v for k, v in data.items() if k != "explanation"})
                            elif "not financial advice" in explanation.lower() or "educational purposes" in explanation.lower():
                                self.log_test(f"Chart Analysis ({test_data['experience_level']})", 
                                            True, "Analysis completed successfully with proper disclaimer", 
                                            {k: v for k, v in data.items() if k != "explanation"})
                            else:
                                # This would be concerning - AI provided analysis without disclaimer
                                self.log_test(f"Chart Analysis ({test_data['experience_level']})", 
                                            False, f"Unexpected AI response: {explanation[:100]}...")
                                all_passed = False
                        else:
                            missing_tp_fields = [f for f in trading_plan_fields if f not in trading_plan]
                            self.log_test(f"Chart Analysis ({test_data['experience_level']})", 
                                        False, f"Missing trading_plan fields: {missing_tp_fields}")
                            all_passed = False
                    else:
                        self.log_test(f"Chart Analysis ({test_data['experience_level']})", 
                                    False, f"Missing required fields: {missing_fields}")
                        all_passed = False
                        
                elif response.status_code == 500:
                    # Check if it's an AI service configuration error
                    error_text = response.text.lower()
                    if "ai service not configured" in error_text or "emergent_llm_key" in error_text:
                        self.log_test(f"Chart Analysis ({test_data['experience_level']})", 
                                    False, "CRITICAL: Emergent LLM key not configured or invalid")
                        all_passed = False
                    else:
                        self.log_test(f"Chart Analysis ({test_data['experience_level']})", 
                                    False, f"Server error: {response.text}")
                        all_passed = False
                else:
                    self.log_test(f"Chart Analysis ({test_data['experience_level']})", 
                                False, f"HTTP {response.status_code}: {response.text}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Chart Analysis ({test_data['experience_level']})", 
                            False, f"Request error: {str(e)}")
                all_passed = False
                
        return all_passed
        
    def test_analysis_history(self):
        """Test GET /api/analysis-history - Get recent analysis history"""
        try:
            response = self.session.get(f"{BASE_URL}/analysis-history", timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    if len(data) > 0:
                        # Check structure of first analysis
                        first_analysis = data[0]
                        required_fields = [
                            "id", "patterns_detected", "support_levels", 
                            "resistance_levels", "trend_analysis", "trading_plan", 
                            "explanation", "experience_level", "created_at"
                        ]
                        
                        missing_fields = [f for f in required_fields if f not in first_analysis]
                        if not missing_fields:
                            self.log_test("Analysis History", True, 
                                        f"Retrieved {len(data)} analysis records", 
                                        {"count": len(data), "sample_fields": list(first_analysis.keys())})
                            return True
                        else:
                            self.log_test("Analysis History", False, 
                                        f"Invalid analysis structure, missing: {missing_fields}")
                            return False
                    else:
                        self.log_test("Analysis History", True, 
                                    "No analysis history found (empty database)", {"count": 0})
                        return True
                else:
                    self.log_test("Analysis History", False, 
                                f"Expected list, got: {type(data)}")
                    return False
            else:
                self.log_test("Analysis History", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Analysis History", False, f"Request error: {str(e)}")
            return False
            
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        all_passed = True
        
        # Test invalid chart analysis request (missing image)
        try:
            response = self.session.post(
                f"{BASE_URL}/analyze-chart",
                json={"experience_level": "beginner"},  # Missing image_base64
                timeout=TIMEOUT
            )
            
            if response.status_code in [400, 422]:  # Expected error codes
                self.log_test("Error Handling - Missing Image", True, 
                            f"Correctly rejected invalid request: HTTP {response.status_code}")
            else:
                self.log_test("Error Handling - Missing Image", False, 
                            f"Unexpected response to invalid request: HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Error Handling - Missing Image", False, f"Request error: {str(e)}")
            all_passed = False
            
        # Test invalid user preferences
        try:
            response = self.session.post(
                f"{BASE_URL}/user-preferences",
                json={"invalid_field": "test"},  # Missing experience_level
                timeout=TIMEOUT
            )
            
            if response.status_code in [400, 422]:  # Expected error codes
                self.log_test("Error Handling - Invalid Preferences", True, 
                            f"Correctly rejected invalid preferences: HTTP {response.status_code}")
            else:
                self.log_test("Error Handling - Invalid Preferences", False, 
                            f"Unexpected response to invalid preferences: HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Error Handling - Invalid Preferences", False, f"Request error: {str(e)}")
            all_passed = False
            
        return all_passed
        
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("=" * 60)
        print("ChartAI Trading Assistant Backend Test Suite")
        print("=" * 60)
        print(f"Testing against: {BASE_URL}")
        print(f"Started at: {datetime.now().isoformat()}")
        print()
        
        # Run tests in logical order
        tests = [
            ("Root Endpoint", self.test_root_endpoint),
            ("User Preferences Save", self.test_save_user_preferences),
            ("User Preferences Get", self.test_get_user_preferences),
            ("Chart Analysis", self.test_chart_analysis),
            ("Analysis History", self.test_analysis_history),
            ("Error Handling", self.test_error_handling)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n--- Running {test_name} Tests ---")
            if test_func():
                passed += 1
                
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
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
    tester = ChartAITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! Backend is working correctly.")
        exit(0)
    else:
        print("\n⚠️  Some tests failed. Check the results above.")
        exit(1)