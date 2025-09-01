#!/bin/bash

# ChartAI TestFlight Quick Setup Script
# Run this after setting up your Apple Developer account

echo "🚀 ChartAI TestFlight Setup"
echo "=========================="

# Step 1: Install required tools
echo "📦 Installing EAS CLI..."
npm install -g eas-cli
npm install -g @expo/cli

# Step 2: Navigate to frontend
cd frontend

# Step 3: Login to services
echo "🔐 Please login to Expo..."
npx expo login

echo "🔐 Please login to EAS..."
eas login

# Step 4: Configure EAS
echo "⚙️ Configuring EAS build..."
eas build:configure

# Step 5: Update app configuration
echo "📝 Please update the following in app.json:"
echo "  - Change bundleIdentifier to: com.yourdomain.chartai"
echo "  - Update any other app details"
echo ""
echo "📝 Please update the following in eas.json:"
echo "  - Add your Apple ID"
echo "  - Add your Apple Team ID"
echo "  - Add your App Store Connect App ID"
echo ""

read -p "Press Enter after updating app.json and eas.json..."

# Step 6: Build for iOS
echo "🏗️ Starting iOS build for TestFlight..."
echo "This will take 10-15 minutes..."
eas build --platform ios --profile production

echo ""
echo "✅ Build started! You can monitor progress at:"
echo "   https://expo.dev/builds"
echo ""
echo "📱 Next steps:"
echo "1. Wait for build to complete"
echo "2. Run: eas submit --platform ios --profile production"
echo "3. Configure your app in App Store Connect"
echo "4. Set up TestFlight testing"
echo ""
echo "📖 See TESTFLIGHT_DEPLOYMENT.md for detailed instructions"