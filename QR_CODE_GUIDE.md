# 📱 Finding Your Expo Go QR Code

## 🎯 **Step-by-Step Guide**

### **Step 1: Start the Development Server**
Open your terminal and run:
```bash
cd /workspace/frontend
npm start
```

### **Step 2: Look for the QR Code**
After running `npm start`, you should see output like this in your terminal:

```
Starting Metro Bundler...
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█ ▄▄▄▄▄ █▀█ █▄▀▀▄▀▄▀█ █ ▄▄▄▄▄ █
█ █   █ █▀▀▀█  ▀▄▀▄▀  █ █   █ █
█ █▄▄▄█ █▀ █▀▀▄▄▀▀▄▀▄ █ █▄▄▄█ █
█▄▄▄▄▄▄▄█▄▀ ▀▄█ █▄█ ▀▄█▄▄▄▄▄▄▄█
█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█ ▄▄▄▄▄ █▀█ █▄▀▀▄▀▄▀█ █ ▄▄▄▄▄ █
█ █   █ █▀▀▀█  ▀▄▀▄▀  █ █   █ █
█ █▄▄▄█ █▀ █▀▀▄▄▀▀▄▀▄ █ █▄▄▄█ █
█▄▄▄▄▄▄▄█▄▀ ▀▄█ █▄█ ▀▄█▄▄▄▄▄▄▄█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

› Metro waiting on exp://192.168.1.100:8081
› Scan the QR code above with Expo Go (Android) or the Camera app (iOS)

› Press a │ open Android
› Press i │ open iOS simulator  
› Press w │ open web

› Press r │ reload app
› Press m │ toggle menu
› Press d │ show developer menu
› Press shift+d │ toggle auto opening developer menu
› Press j │ open debugger
› Press c │ clear cache and restart
```

### **Step 3: What to Look For**

The QR code is the **square pattern made of black and white blocks** that appears in your terminal. It looks like this:
```
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█ ▄▄▄▄▄ █▀█ █▄▀▀▄▀▄▀█ █ ▄▄▄▄▄ █
█ █   █ █▀▀▀█  ▀▄▀▄▀  █ █   █ █
█ █▄▄▄█ █▀ █▀▀▄▄▀▀▄▀▄ █ █▄▄▄█ █
█▄▄▄▄▄▄▄█▄▀ ▀▄█ █▄█ ▀▄█▄▄▄▄▄▄▄█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
```

## 📱 **How to Use the QR Code**

### **For iOS (iPhone/iPad):**
1. Open the **Camera app** (built-in camera)
2. Point it at the QR code in your terminal
3. Tap the notification that appears
4. This will open Expo Go and load your app

### **For Android:**
1. Install **Expo Go** from Google Play Store
2. Open Expo Go app
3. Tap "Scan QR Code"
4. Point camera at the QR code in your terminal
5. Your app will load

## 🔧 **Troubleshooting**

### **If you don't see the QR code:**

1. **Make sure you're in the right directory:**
   ```bash
   cd /workspace/frontend
   npm start
   ```

2. **Clear the terminal and try again:**
   ```bash
   clear
   npm start
   ```

3. **If the terminal is too small, make it bigger:**
   - The QR code needs space to display
   - Expand your terminal window

4. **Try the web version instead:**
   ```bash
   npm run web
   ```
   Then open `http://localhost:8081` in your browser

### **Alternative: Manual Connection**

If the QR code doesn't work, you can connect manually:

1. **Find your computer's IP address:**
   ```bash
   # On Mac/Linux:
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # On Windows:
   ipconfig
   ```

2. **Open Expo Go on your phone**
3. **Tap "Enter URL manually"**
4. **Type:** `exp://YOUR_IP_ADDRESS:8081`
   (Replace YOUR_IP_ADDRESS with your computer's IP)

## 🌐 **Web Alternative**

If you can't use your phone right now, you can preview the app in your web browser:

```bash
cd /workspace/frontend
npm run web
```

Then open: `http://localhost:8081`

**Note:** Camera features won't work in the browser, but you can see the UI and test navigation.

## 📱 **What You Should See**

Once connected, you should see:
1. **Welcome screen** with ChartAI branding
2. **Experience level selection** (Beginner/Intermediate/Advanced)
3. **Upload screen** with camera and gallery options
4. **Mock analysis results** with charts and visualizations

## 🎯 **Expected Timeline**

- **Terminal startup**: 10-30 seconds
- **QR code appears**: Immediately after startup
- **Phone connection**: 5-10 seconds after scanning
- **App loads**: 10-20 seconds first time

## 💡 **Pro Tips**

1. **Keep terminal open** - closing it stops the server
2. **Stay on same WiFi** - phone and computer must be on same network
3. **Try different terminals** - some display QR codes better than others
4. **Use good lighting** - make sure camera can see the QR code clearly
5. **Install Expo Go first** - download from App Store/Play Store before scanning

## 🆘 **Still Can't Find It?**

If you still don't see the QR code:

1. **Take a screenshot** of your terminal output
2. **Check if there are error messages** in the terminal
3. **Try running:** `npx expo start --tunnel` (uses ngrok for connection)
4. **Or use the web version** as a backup

The QR code is essential for mobile testing - it's how Expo Go connects to your development server!