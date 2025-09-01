# 🧪 ChartAI Testing Guide

## 🚀 **Quick Testing Methods**

### Method 1: **Expo Development Testing** (Recommended)

1. **Start the Frontend:**
   ```bash
   cd frontend
   npm start
   ```
   
2. **Start the Backend:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn server_openai:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Test on Device:**
   - Install **Expo Go** app on your phone
   - Scan the QR code from the terminal
   - Test all features directly on your device

### Method 2: **Web Browser Testing**

1. **Start Frontend with Web Support:**
   ```bash
   cd frontend
   npm run web
   ```
   
2. **Open in Browser:**
   - Visit: `http://localhost:8081`
   - Test basic functionality in web browser
   - Note: Camera features may be limited in browser

### Method 3: **iOS Simulator Testing**

1. **Install Xcode** (Mac only)
2. **Start iOS Simulator:**
   ```bash
   cd frontend
   npm run ios
   ```

### Method 4: **Android Emulator Testing**

1. **Install Android Studio**
2. **Start Android Emulator:**
   ```bash
   cd frontend
   npm run android
   ```

## 🧪 **Automated Testing**

### Backend API Testing
```bash
# Run comprehensive backend tests
python test_chartai.py

# Check specific endpoints
curl -X GET http://localhost:8000/api/health
curl -X POST http://localhost:8000/api/user-preferences \
  -H "Content-Type: application/json" \
  -d '{"experience_level": "intermediate"}'
```

### Frontend Component Testing
```bash
cd frontend
npm test  # If you add Jest testing later
```

## 📱 **Manual Testing Scenarios**

### **Scenario 1: New User Onboarding**
1. Open app for first time
2. Select experience level (try all 3 levels)
3. Verify navigation to upload screen
4. Check that selection is saved

### **Scenario 2: Chart Upload & Analysis**
1. Take a photo of a chart (or use sample images)
2. Upload the image
3. Wait for AI analysis
4. Review results for:
   - Pattern detection
   - Support/resistance levels
   - Trading plan
   - Appropriate explanation for your level
   - Financial disclaimer presence

### **Scenario 3: Experience Level Testing**
1. Upload the same chart with different experience levels
2. Compare the explanations:
   - **Beginner**: Simple language, basic concepts
   - **Intermediate**: Technical terms, moderate complexity
   - **Advanced**: Professional terminology, detailed analysis

### **Scenario 4: Error Handling**
1. Try uploading non-chart images
2. Test with poor internet connection
3. Test with very large/small images
4. Verify error messages are user-friendly

## 📊 **Sample Test Images**

Create these test scenarios:

### **Good Test Images:**
- Clear stock charts with visible price levels
- Crypto charts with support/resistance lines
- Forex charts with trend patterns
- Screenshots from trading platforms

### **Edge Case Images:**
- Blurry or low-quality charts
- Charts with no visible price levels
- Non-financial images (should be handled gracefully)
- Very large images (>5MB)
- Very small images (<50KB)

## 🔧 **Development Testing Setup**

### **Environment Variables Setup:**

1. **Backend (.env):**
   ```env
   MONGO_URL=mongodb://localhost:27017
   DB_NAME=chartai_test
   OPENAI_API_KEY=your_openai_key_here  # Optional for testing
   EMERGENT_LLM_KEY=your_emergent_key   # If available
   ```

2. **Frontend (.env):**
   ```env
   EXPO_PUBLIC_BACKEND_URL=http://localhost:8000
   # For device testing, use your computer's IP:
   # EXPO_PUBLIC_BACKEND_URL=http://192.168.1.100:8000
   ```

### **Database Testing:**
```bash
# Install MongoDB locally or use MongoDB Atlas
# Test database connection:
python -c "from motor.motor_asyncio import AsyncIOMotorClient; print('DB OK')"
```

## 📱 **Device-Specific Testing**

### **iOS Testing:**
- Test on iPhone and iPad
- Check camera permissions
- Verify image picker functionality
- Test navigation and gestures

### **Android Testing:**
- Test on various Android versions
- Check different screen sizes
- Verify camera and storage permissions
- Test back button behavior

## 🔍 **Performance Testing**

### **Load Testing:**
```bash
# Test multiple simultaneous requests
for i in {1..5}; do
  curl -X GET http://localhost:8000/api/health &
done
wait
```

### **Image Processing Testing:**
- Upload various image sizes
- Test processing time for different chart types
- Monitor memory usage during analysis

## 🐛 **Debugging & Troubleshooting**

### **Common Issues:**

1. **"Network Error" in App:**
   - Check backend is running on correct port
   - Verify EXPO_PUBLIC_BACKEND_URL is correct
   - For device testing, use computer's IP address

2. **"Cannot connect to backend":**
   - Ensure both devices are on same WiFi network
   - Check firewall settings
   - Try using ngrok for tunneling

3. **"AI Analysis Failed":**
   - Check OpenAI API key is valid
   - Monitor backend logs for errors
   - Verify image base64 encoding is correct

4. **"Camera not working":**
   - Check app permissions
   - Try on physical device (camera doesn't work in simulator)
   - Verify Expo ImagePicker is properly configured

### **Debug Commands:**
```bash
# Check backend logs
cd backend && uvicorn server_openai:app --reload --log-level debug

# Check frontend logs
cd frontend && npm start -- --clear

# Test API directly
curl -X POST http://localhost:8000/api/analyze-chart \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "test", "experience_level": "beginner"}'
```

## 📈 **Testing Metrics**

Track these metrics during testing:

### **Performance Metrics:**
- App startup time (target: <3 seconds)
- Image upload time (target: <5 seconds)
- AI analysis time (target: <30 seconds)
- UI responsiveness (smooth 60fps scrolling)

### **Quality Metrics:**
- AI analysis accuracy (subjective evaluation)
- User experience flow completion rate
- Error rate and recovery success
- Cross-platform consistency

### **Compliance Metrics:**
- Financial disclaimer presence (100%)
- Appropriate warning messages
- Educational content quality
- Legal compliance verification

## 🎯 **Testing Checklist**

### **Pre-Release Testing:**
- [ ] All automated tests pass
- [ ] Manual testing completed on iOS
- [ ] Manual testing completed on Android
- [ ] Performance benchmarks met
- [ ] Error handling verified
- [ ] Legal disclaimers confirmed
- [ ] User experience flow tested
- [ ] AI analysis quality validated

### **Production Readiness:**
- [ ] Environment variables configured
- [ ] Database connections secure
- [ ] API keys properly managed
- [ ] Error logging implemented
- [ ] Analytics tracking ready
- [ ] App store metadata prepared

## 🚀 **Next Steps After Testing**

1. **Fix any identified issues**
2. **Optimize performance bottlenecks**
3. **Prepare for app store submission**
4. **Set up production monitoring**
5. **Plan user feedback collection**

## 📞 **Getting Help**

If you encounter issues:
1. Check the logs in both frontend and backend
2. Review the automated test results
3. Consult the manual testing checklist
4. Verify environment configuration
5. Test with sample data first

Remember: The app includes mock data fallbacks, so basic testing will work even without API keys!