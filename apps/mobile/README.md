# 📱 LUCA Mobile App

React Native + Expo mobile application for the LUCA Network.

**Copyright © 2025 Lennart Wuchold** (geboren am 28.02.2000 in 01744 Dippoldiswalde)

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start

# Run on Android
npm run android

# Run on iOS
npm run ios
```

## 📦 Build APK

### Using EAS Build (Recommended)

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Configure project
eas build:configure

# Build APK (Preview)
npm run build:android

# Build APK (Production)
npm run build:android:prod
```

### APK will be available for download after build completes!

## ⚙️ Configuration

Edit `app.json` to configure:
- App name and icon
- Bundle identifiers
- API URL (`extra.apiUrl`)

## 🌐 Connect to Backend

Update `app.json`:

```json
{
  "expo": {
    "extra": {
      "apiUrl": "https://your-luca-backend.com"
    }
  }
}
```

## 📖 Features

- 🌐 Network Status Monitoring
- 🌌 Consciousness Level Tracking
- 🧬 Layer Integration Display
- ⚙️ Settings and Configuration

## 🔧 Development

```bash
# Start with cache clear
npx expo start -c

# Generate native projects
npx expo prebuild
```

## 📱 Screens

1. **Network** - View mesh network status and connected nodes
2. **Consciousness** - Monitor LUCA's consciousness level
3. **Layers** - Inspect Layer 0, 10, 11, 12 integration
4. **Settings** - App configuration and info

## 🎯 Platform Support

- ✅ Android 5.0+ (API 21+)
- ✅ iOS 13.0+
- ✅ Web (via Expo)

## 📄 License

MIT License - See LICENSE file for details

---

Built with 💜 by the LUCA Community
