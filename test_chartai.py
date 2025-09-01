#!/usr/bin/env python3
"""
ChartAI Testing Framework
Automated testing for ChartAI mobile app functionality
"""

import asyncio
import aiohttp
import base64
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

class ChartAITester:
    def __init__(self, backend_url: str = "https://trade-vision-7.preview.emergentagent.com"):
        self.backend_url = backend_url
        self.test_results = []
        
    async def test_backend_health(self) -> Dict:
        """Test if backend is healthy and responding"""
        test_name = "Backend Health Check"
        start_time = datetime.now()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/api/health") as response:
                    if response.status == 200:
                        result = {
                            "test": test_name,
                            "status": "PASS",
                            "message": "Backend is healthy",
                            "duration": (datetime.now() - start_time).total_seconds()
                        }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "message": f"Backend returned status {response.status}",
                            "duration": (datetime.now() - start_time).total_seconds()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "FAIL",
                "message": f"Backend connection failed: {str(e)}",
                "duration": (datetime.now() - start_time).total_seconds()
            }
        
        self.test_results.append(result)
        return result
    
    async def test_user_preferences(self) -> Dict:
        """Test user preferences endpoint"""
        test_name = "User Preferences API"
        start_time = datetime.now()
        
        try:
            test_data = {"experience_level": "intermediate"}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.backend_url}/api/user-preferences",
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "id" in data and data.get("experience_level") == "intermediate":
                            result = {
                                "test": test_name,
                                "status": "PASS",
                                "message": "User preferences created successfully",
                                "duration": (datetime.now() - start_time).total_seconds()
                            }
                        else:
                            result = {
                                "test": test_name,
                                "status": "FAIL",
                                "message": "Invalid response format",
                                "duration": (datetime.now() - start_time).total_seconds()
                            }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "message": f"API returned status {response.status}",
                            "duration": (datetime.now() - start_time).total_seconds()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "FAIL",
                "message": f"Test failed: {str(e)}",
                "duration": (datetime.now() - start_time).total_seconds()
            }
        
        self.test_results.append(result)
        return result
    
    def create_test_image_base64(self) -> str:
        """Create a simple test image as base64"""
        # Create a simple 100x100 white image
        from PIL import Image
        import io
        
        img = Image.new('RGB', (100, 100), color='white')
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        img_bytes = buffer.getvalue()
        return base64.b64encode(img_bytes).decode('utf-8')
    
    async def test_chart_analysis(self) -> Dict:
        """Test chart analysis endpoint"""
        test_name = "Chart Analysis API"
        start_time = datetime.now()
        
        try:
            # Create test image
            test_image = self.create_test_image_base64()
            test_data = {
                "image_base64": test_image,
                "experience_level": "beginner"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.backend_url}/api/analyze-chart",
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        required_fields = ["id", "patterns_detected", "support_levels", 
                                         "resistance_levels", "trend_analysis", "trading_plan"]
                        
                        missing_fields = [field for field in required_fields if field not in data]
                        
                        if not missing_fields:
                            result = {
                                "test": test_name,
                                "status": "PASS",
                                "message": "Chart analysis completed successfully",
                                "duration": (datetime.now() - start_time).total_seconds()
                            }
                        else:
                            result = {
                                "test": test_name,
                                "status": "FAIL",
                                "message": f"Missing required fields: {missing_fields}",
                                "duration": (datetime.now() - start_time).total_seconds()
                            }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "message": f"API returned status {response.status}",
                            "duration": (datetime.now() - start_time).total_seconds()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "FAIL",
                "message": f"Test failed: {str(e)}",
                "duration": (datetime.now() - start_time).total_seconds()
            }
        
        self.test_results.append(result)
        return result
    
    async def test_experience_levels(self) -> Dict:
        """Test different experience levels produce different outputs"""
        test_name = "Experience Level Differentiation"
        start_time = datetime.now()
        
        try:
            test_image = self.create_test_image_base64()
            levels = ["beginner", "intermediate", "advanced"]
            responses = {}
            
            async with aiohttp.ClientSession() as session:
                for level in levels:
                    test_data = {
                        "image_base64": test_image,
                        "experience_level": level
                    }
                    
                    async with session.post(
                        f"{self.backend_url}/api/analyze-chart",
                        json=test_data,
                        headers={"Content-Type": "application/json"}
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            responses[level] = data.get("explanation", "")
                        else:
                            raise Exception(f"Failed to get response for {level} level")
                
                # Check if responses are different
                if len(set(responses.values())) == len(levels):
                    result = {
                        "test": test_name,
                        "status": "PASS",
                        "message": "Different experience levels produce different outputs",
                        "duration": (datetime.now() - start_time).total_seconds()
                    }
                else:
                    result = {
                        "test": test_name,
                        "status": "FAIL",
                        "message": "Experience levels produce identical outputs",
                        "duration": (datetime.now() - start_time).total_seconds()
                    }
                    
        except Exception as e:
            result = {
                "test": test_name,
                "status": "FAIL",
                "message": f"Test failed: {str(e)}",
                "duration": (datetime.now() - start_time).total_seconds()
            }
        
        self.test_results.append(result)
        return result
    
    def check_disclaimer_presence(self, text: str) -> bool:
        """Check if financial disclaimer is present in text"""
        disclaimer_keywords = [
            "not financial advice",
            "educational purposes",
            "not financial advice",
            "educational only"
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in disclaimer_keywords)
    
    async def test_disclaimer_presence(self) -> Dict:
        """Test that financial disclaimers are present"""
        test_name = "Financial Disclaimer Check"
        start_time = datetime.now()
        
        try:
            test_image = self.create_test_image_base64()
            test_data = {
                "image_base64": test_image,
                "experience_level": "beginner"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.backend_url}/api/analyze-chart",
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        explanation = data.get("explanation", "")
                        
                        if self.check_disclaimer_presence(explanation):
                            result = {
                                "test": test_name,
                                "status": "PASS",
                                "message": "Financial disclaimer found in response",
                                "duration": (datetime.now() - start_time).total_seconds()
                            }
                        else:
                            result = {
                                "test": test_name,
                                "status": "FAIL",
                                "message": "Financial disclaimer missing from response",
                                "duration": (datetime.now() - start_time).total_seconds()
                            }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "message": f"API returned status {response.status}",
                            "duration": (datetime.now() - start_time).total_seconds()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "FAIL",
                "message": f"Test failed: {str(e)}",
                "duration": (datetime.now() - start_time).total_seconds()
            }
        
        self.test_results.append(result)
        return result
    
    async def run_all_tests(self) -> Dict:
        """Run all automated tests"""
        print("🚀 Starting ChartAI Automated Tests...")
        print("=" * 50)
        
        tests = [
            self.test_backend_health,
            self.test_user_preferences,
            self.test_chart_analysis,
            self.test_experience_levels,
            self.test_disclaimer_presence
        ]
        
        for test in tests:
            print(f"Running {test.__name__.replace('test_', '').replace('_', ' ').title()}...")
            result = await test()
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_icon} {result['test']}: {result['message']} ({result['duration']:.2f}s)")
        
        # Summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = total_tests - passed_tests
        
        print("\n" + "=" * 50)
        print(f"📊 Test Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        return {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": (passed_tests/total_tests)*100,
            "results": self.test_results
        }

async def main():
    """Main test runner"""
    tester = ChartAITester()
    results = await tester.run_all_tests()
    
    # Save results to file
    with open("/workspace/test_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved to: test_results.json")
    
    # Exit with error code if tests failed
    if results["failed"] > 0:
        sys.exit(1)
    else:
        print("\n🎉 All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())