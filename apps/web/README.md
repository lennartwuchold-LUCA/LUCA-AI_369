# LUCA Web App - Complete Full-Stack Implementation

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 📦 Deployment

### Option 1: Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Option 2: Docker
```bash
# Build Docker image
docker build -t luca-webapp .

# Run container
docker run -p 3000:3000 luca-webapp
```

### Option 3: Traditional Server
```bash
# Build
npm run build

# Copy .next, public, package.json to server
# On server:
npm install --production
npm start
```

## 🌍 Access

After deployment:
- Local: http://localhost:3000
- Production: https://your-domain.com

## 📱 Features

- Real-time mesh network visualization
- Cultural context integration
- Responsive design (desktop/tablet/mobile)
- PWA support (installable)
- Offline-first architecture

## 🔧 Environment Variables

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws
```

## 📊 Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- WebSocket for real-time
- PWA support
