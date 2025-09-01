# 🚀 TestFlight Deployment Guide for ChartAI

## 📋 **Prerequisites Checklist**

- [ ] Apple Developer Account ($99/year) - [Sign up here](https://developer.apple.com)
- [ ] Mac computer with Xcode 14+ installed
- [ ] EAS CLI installed globally
- [ ] Your backend deployed and accessible via HTTPS

## 🔧 **Step 1: Setup and Configuration**

### **1.1 Install EAS CLI**
```bash
npm install -g eas-cli
npm install -g @expo/cli
```

### **1.2 Login to Expo**
```bash
cd frontend
npx expo login
eas login
```

### **1.3 Update Bundle Identifier**
Edit `app.json` and change:
```json
"bundleIdentifier": "com.yourcompany.chartai"
```
To your unique identifier:
```json
"bundleIdentifier": "com.yourdomain.chartai"
```

### **1.4 Update EAS Configuration**
Edit `eas.json` and add your Apple Developer details:
```json
{
  "submit": {
    "production": {
      "ios": {
        "appleId": "your-apple-id@example.com",
        "ascAppId": "your-app-store-connect-app-id", 
        "appleTeamId": "your-apple-team-id"
      }
    }
  }
}
```

## 🏗️ **Step 2: Backend Deployment**

### **Option A: Deploy to Railway (Recommended)**
1. Create account at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Deploy backend with environment variables:
   ```env
   MONGO_URL=your-mongodb-atlas-url
   DB_NAME=chartai_production
   OPENAI_API_KEY=your-openai-key
   ```

### **Option B: Deploy to Heroku**
```bash
# Install Heroku CLI
cd backend
heroku create your-chartai-backend
heroku config:set MONGO_URL=your-mongodb-url
heroku config:set OPENAI_API_KEY=your-openai-key
git push heroku main
```

### **Option C: Deploy to DigitalOcean/AWS**
- Use Docker container with your backend
- Set up MongoDB Atlas for database
- Configure environment variables

## 📱 **Step 3: Configure Frontend for Production**

### **3.1 Update Environment Variables**
Create `frontend/.env.production`:
```env
EXPO_PUBLIC_BACKEND_URL=https://your-backend-domain.com
```

### **3.2 Update App Metadata**
Ensure your `app.json` has:
```json
{
  "expo": {
    "name": "ChartAI",
    "description": "Smart Trading Assistant - AI-powered chart analysis for educational purposes",
    "privacy": "public",
    "ios": {
      "bundleIdentifier": "com.yourdomain.chartai",
      "buildNumber": "1",
      "infoPlist": {
        "NSCameraUsageDescription": "ChartAI needs camera access to capture trading charts for analysis",
        "NSPhotoLibraryUsageDescription": "ChartAI needs photo library access to select trading charts for analysis"
      }
    }
  }
}
```

## 🏗️ **Step 4: Build for iOS**

### **4.1 Configure EAS Build**
```bash
cd frontend
eas build:configure
```

### **4.2 Create iOS Build**
```bash
# For TestFlight (production build)
eas build --platform ios --profile production

# For internal testing (faster)
eas build --platform ios --profile preview
```

This will:
- Create/update certificates automatically
- Build your app in the cloud
- Generate an `.ipa` file for TestFlight

### **4.3 Monitor Build Progress**
- Watch the build logs in your terminal
- Or visit [expo.dev/builds](https://expo.dev/builds)
- Build typically takes 10-15 minutes

## 📲 **Step 5: Submit to TestFlight**

### **Option A: Automatic Submission (Recommended)**
```bash
eas submit --platform ios --profile production
```

### **Option B: Manual Upload via Xcode**
1. Download the `.ipa` file from your EAS build
2. Open Xcode
3. Go to Window → Organizer
4. Drag the `.ipa` file to upload
5. Click "Distribute App" → "App Store Connect"

### **Option C: Manual Upload via Transporter**
1. Download Apple Transporter from Mac App Store
2. Download your `.ipa` file
3. Drag `.ipa` to Transporter
4. Click "Deliver"

## 🍎 **Step 6: App Store Connect Configuration**

### **6.1 Create App in App Store Connect**
1. Go to [appstoreconnect.apple.com](https://appstoreconnect.apple.com)
2. Click "My Apps" → "+" → "New App"
3. Fill in:
   - **Name**: ChartAI
   - **Bundle ID**: com.yourdomain.chartai
   - **SKU**: chartai-2024
   - **User Access**: Full Access

### **6.2 App Information**
- **Name**: ChartAI - Smart Trading Assistant
- **Subtitle**: AI-Powered Chart Analysis
- **Category**: Finance
- **Content Rights**: No, it does not contain, show, or access third-party content

### **6.3 App Privacy**
Configure privacy practices:
- **Camera**: Used for capturing chart images
- **Photos**: Used for selecting chart images
- **Device ID**: Not collected
- **Usage Data**: Not collected

### **6.4 App Review Information**
```
Contact Information:
- First Name: [Your Name]
- Last Name: [Your Last Name]
- Phone Number: [Your Phone]
- Email: [Your Email]

Demo Account: Not required

Notes:
ChartAI is an educational tool for learning technical analysis. 
All analysis provided is for educational purposes only and is not financial advice.
The app requires camera access to capture trading charts for AI analysis.
```

## 🧪 **Step 7: TestFlight Setup**

### **7.1 Internal Testing**
1. In App Store Connect, go to TestFlight
2. Select your app
3. Under "Internal Testing", add team members
4. They'll receive an email to download TestFlight

### **7.2 External Testing**
1. Create an External Test group
2. Add up to 10,000 external testers
3. Provide test information:
   ```
   What to Test:
   - Upload and analyze trading charts
   - Test different experience levels (Beginner/Intermediate/Advanced)
   - Verify AI analysis quality and educational content
   - Check that financial disclaimers are prominently displayed
   
   Test Instructions:
   1. Select your trading experience level
   2. Take a photo of a trading chart or upload from gallery
   3. Wait for AI analysis (may take 30 seconds)
   4. Review the analysis results and trading plan
   5. Try different chart types (stocks, crypto, forex)
   ```

## 📝 **Step 8: App Store Metadata**

### **8.1 App Store Description**
```
ChartAI - Smart Trading Assistant

Transform your trading education with AI-powered chart analysis!

🧠 INTELLIGENT ANALYSIS
• Advanced pattern recognition
• Support and resistance identification  
• Trend analysis and market insights
• Personalized trading plans with entry/exit recommendations

📚 EDUCATIONAL FOCUS
• Explanations tailored to your experience level
• Learn technical analysis concepts
• Understand market patterns and structures
• Risk management education

📱 EASY TO USE
• Take photos of any trading chart
• Upload from your photo library
• Get analysis in seconds
• Clear, actionable insights

⚠️ IMPORTANT DISCLAIMER
All analysis provided is for educational purposes only and is not financial advice. 
Users should conduct their own research before making investment decisions.

FEATURES:
✓ Camera integration for chart capture
✓ AI-powered pattern detection
✓ Support/resistance level identification
✓ Risk/reward calculations
✓ Experience-based explanations
✓ Multiple chart type support (stocks, crypto, forex)
✓ Clean, professional interface

Perfect for traders and investors looking to enhance their technical analysis skills!
```

### **8.2 Keywords**
```
trading,chart analysis,technical analysis,stocks,crypto,forex,AI,education,patterns,support,resistance,finance
```

### **8.3 Screenshots**
You'll need to create screenshots showing:
1. Onboarding/experience selection
2. Chart upload interface
3. Analysis results with charts
4. Trading plan display
5. Settings screen

## 🚀 **Step 9: Launch Process**

### **9.1 TestFlight Beta Testing**
1. Upload first build
2. Add internal testers (your team)
3. Test thoroughly for 1-2 weeks
4. Add external testers
5. Gather feedback and iterate

### **9.2 App Store Review**
1. Submit for App Review when ready
2. Typical review time: 24-48 hours
3. Address any review feedback
4. Release when approved

## 🔧 **Step 10: Continuous Deployment**

### **10.1 Update Process**
```bash
# Update version in app.json
# Increment buildNumber for iOS
eas build --platform ios --profile production
eas submit --platform ios --profile production
```

### **10.2 Version Management**
- **Version**: 1.0.0, 1.0.1, 1.1.0 (semantic versioning)
- **Build Number**: 1, 2, 3, 4 (increment for each build)

## 🛠️ **Troubleshooting Common Issues**

### **Build Failures**
```bash
# Clear cache and retry
eas build --clear-cache --platform ios

# Check build logs
eas build:list
```

### **Certificate Issues**
```bash
# Reset certificates
eas credentials --platform ios --clear-provisioning-profile
eas credentials --platform ios --clear-dist-cert
```

### **Environment Variables**
- Ensure production backend URL is HTTPS
- Verify all API keys are properly set
- Test backend endpoints manually

### **App Store Rejection**
Common reasons:
- Missing privacy policy
- Unclear app purpose
- Financial advice concerns (ensure disclaimers are prominent)
- Broken functionality

## 📊 **Testing Checklist Before Submission**

- [ ] App launches successfully
- [ ] Camera permissions work
- [ ] Image upload functions properly
- [ ] AI analysis returns results
- [ ] All experience levels work correctly
- [ ] Financial disclaimers are prominent
- [ ] Error handling works gracefully
- [ ] App doesn't crash under normal use
- [ ] Backend is stable and accessible
- [ ] Performance is acceptable (< 3s launch)

## 🎯 **Timeline Expectations**

- **EAS Build**: 10-15 minutes
- **TestFlight Processing**: 10-30 minutes
- **Internal Testing**: 1-2 weeks
- **External Testing**: 2-4 weeks
- **App Store Review**: 24-48 hours
- **Total Time to Launch**: 4-6 weeks

## 💡 **Pro Tips**

1. **Start with internal testing** - catch obvious issues early
2. **Use semantic versioning** - makes tracking easier
3. **Test on multiple devices** - iPhone and iPad
4. **Prepare marketing materials** early
5. **Have a privacy policy** ready (required for App Store)
6. **Monitor crash reports** in App Store Connect
7. **Respond to user reviews** promptly

## 🔗 **Useful Resources**

- [Expo EAS Documentation](https://docs.expo.dev/build/introduction/)
- [App Store Connect Help](https://help.apple.com/app-store-connect/)
- [TestFlight Documentation](https://developer.apple.com/testflight/)
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)

Remember: The key to successful TestFlight deployment is thorough testing and clear communication about your app's educational purpose!