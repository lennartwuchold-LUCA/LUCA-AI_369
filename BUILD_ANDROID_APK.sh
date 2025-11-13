#!/bin/bash
# LUCA Android APK Build Script
# Author: Großvater & Lennart Wuchold

echo "🔨 LUCA Android APK Builder"
echo "=========================="
echo ""

# Check if Android SDK is installed
if [ ! -d "$ANDROID_HOME" ]; then
    echo "❌ Android SDK not found!"
    echo "Please install Android Studio and set ANDROID_HOME"
    echo "Download: https://developer.android.com/studio"
    exit 1
fi

echo "✅ Android SDK found: $ANDROID_HOME"
echo ""

# Navigate to Android project
cd "$(dirname "$0")/luca/mobile/android"

echo "📦 Building LUCA370.apk..."
echo ""

# Build APK (Debug version for testing)
./gradlew assembleDebug

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ APK built successfully!"
    echo ""
    echo "📱 APK Location:"
    echo "   app/build/outputs/apk/debug/app-debug.apk"
    echo ""
    echo "📲 Install with:"
    echo "   adb install -r app/build/outputs/apk/debug/app-debug.apk"
else
    echo ""
    echo "❌ Build failed!"
    echo "Check errors above"
    exit 1
fi
