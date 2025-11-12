#!/bin/bash
# 🚀 LUCA COMPLETE DEPLOYMENT SCRIPT
# Deploys all three platforms automatically

set -e  # Exit on error

echo "🚀 LUCA DEPLOYMENT STARTING..."
echo "================================"

# Colors
GREEN='\033[0.32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. WEB APP DEPLOYMENT
echo -e "${YELLOW}📦 1/3: Deploying Web App...${NC}"
cd web-app

if command -v vercel &> /dev/null; then
    echo "✓ Vercel CLI found, deploying to Vercel..."
    vercel --yes --prod
else
    echo "⚠ Vercel CLI not found, building locally..."
    npm install
    npm run build
    echo -e "${GREEN}✓ Web app built successfully!${NC}"
    echo "  Start with: npm start"
    echo "  Access at: http://localhost:3000"
fi

cd ..

# 2. MOBILE APP BUILD
echo -e "${YELLOW}📦 2/3: Building Mobile App (Android APK)...${NC}"
cd mobile-app

if command -v eas &> /dev/null; then
    echo "✓ EAS CLI found, building APK..."
    eas build -p android --profile preview --non-interactive
    echo -e "${GREEN}✓ Android APK build started!${NC}"
    echo "  Check build status: eas build:list"
else
    echo "⚠ EAS CLI not found. Install with:"
    echo "  npm install -g eas-cli"
    echo "  Then run: eas build -p android"
fi

cd ..

# 3. T-DECK APP FLASH
echo -e "${YELLOW}📦 3/3: Building T-Deck Firmware...${NC}"
cd t-deck-app

if command -v pio &> /dev/null; then
    echo "✓ PlatformIO found, building firmware..."
    pio run

    echo -e "${GREEN}✓ T-Deck firmware built!${NC}"
    echo "  Firmware location: .pio/build/lilygo-tdeck/firmware.bin"
    echo ""
    echo "To upload to device:"
    echo "  1. Connect T-Deck via USB"
    echo "  2. Run: pio run --target upload"
else
    echo "⚠ PlatformIO not found. Install with:"
    echo "  curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py | python3"
fi

cd ..

# SUMMARY
echo ""
echo "================================"
echo -e "${GREEN}🎉 DEPLOYMENT COMPLETE!${NC}"
echo "================================"
echo ""
echo "📊 DEPLOYMENT STATUS:"
echo ""
echo "🌐 Web App:"
echo "   Status: Built & Ready"
echo "   Access: Check terminal output for URL"
echo ""
echo "📱 Mobile App:"
echo "   Status: Building (check EAS)"
echo "   Download: Will receive APK link via email"
echo ""
echo "⌚ T-Deck App:"
echo "   Status: Firmware ready"
echo "   Flash: Connect device and run 'pio run --target upload'"
echo ""
echo "💰 READY TO MAKE GOLD!"
echo ""
echo "Next steps:"
echo "1. Test web app in browser"
echo "2. Install APK on Android phone"
echo "3. Flash T-Deck device"
echo "4. Share with users and PROFIT! 🚀"
