# AstroShield Vercel Deployment Guide

## 🚀 Quick Deployment Steps

### Prerequisites
- Vercel account (sign up at vercel.com)
- Git repository pushed to GitHub/GitLab/Bitbucket

### 1. Deploy to Vercel

**Option A: Via Vercel Dashboard**
1. Go to [vercel.com](https://vercel.com) and log in
2. Click "New Project"
3. Import your AstroSheild repository
4. Vercel will auto-detect the configuration
5. Click "Deploy"

**Option B: Via Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from project root
cd AstroSheild
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? [your account]
# - Link to existing project? N
# - Project name: astroshield
# - Directory: ./
# - Override settings? N
```

### 2. Environment Variables (if needed)
In Vercel dashboard:
1. Go to Project Settings
2. Environment Variables tab
3. Add any required variables

### 3. Custom Domain (Optional)
1. In Vercel dashboard, go to Domains
2. Add your custom domain
3. Configure DNS as instructed

## 📁 Project Structure for Vercel

```
AstroSheild/
├── api/                    # Serverless functions
│   └── index.py           # Main API handler
├── client/                # React frontend
│   ├── dist/             # Build output (auto-generated)
│   ├── src/              # Source code
│   └── package.json      # Frontend dependencies
├── server/               # Original Flask app (reference)
├── vercel.json          # Vercel configuration
└── requirements.txt     # Python dependencies
```

## 🔧 Configuration Files

### vercel.json
- Configures both frontend and backend deployment
- Routes API calls to serverless functions
- Handles static file serving
- Sets up CORS headers

### requirements.txt
- Python dependencies for serverless functions
- Minimal set for optimal cold start times

### Environment Variables
- `REACT_APP_API_URL`: Set to `/api` for production
- Development uses `http://localhost:5000`

## 🌐 API Endpoints (Production)

Once deployed, your API will be available at:
```
https://your-project.vercel.app/api/health
https://your-project.vercel.app/api/info
https://your-project.vercel.app/api/asteroids/433
https://your-project.vercel.app/api/asteroids/search?q=Ceres
https://your-project.vercel.app/api/impact/simulate
```

## 🎯 Frontend Routes

Your React app will be available at:
```
https://your-project.vercel.app/          # Home page
https://your-project.vercel.app/asteroid  # Asteroid page
https://your-project.vercel.app/game      # Game page
```

## ⚡ What Was Changed for Vercel

### Minimal Changes Made:
1. **Added `/api` directory** with serverless function
2. **Created `vercel.json`** configuration
3. **Updated `requirements.txt`** with essential dependencies
4. **Added environment variables** for API URL switching
5. **Simplified API endpoints** for serverless compatibility

### No Changes Required:
- ✅ Your existing React code works as-is
- ✅ Frontend routes remain the same
- ✅ Component structure unchanged
- ✅ Styling and assets work normally

## 🔍 Testing Your Deployment

### 1. Test API Health
```bash
curl https://your-project.vercel.app/api/health
```

### 2. Test Asteroid Data
```bash
curl https://your-project.vercel.app/api/asteroids/433
```

### 3. Test Frontend
Visit `https://your-project.vercel.app` in your browser

## 🛠️ Troubleshooting

### Common Issues:

**Build Fails:**
- Check that all dependencies are in `package.json`
- Ensure `npm run build` works locally

**API Not Working:**
- Check Python dependencies in `requirements.txt`
- Verify API endpoints in browser dev tools

**CORS Issues:**
- CORS is configured in `vercel.json` and API code
- Should work automatically

### Logs and Debugging:
1. Vercel Dashboard → Functions tab → View logs
2. Browser Dev Tools → Network tab for API calls
3. Console for frontend errors

## 🚀 Development vs Production

### Development (Local)
```bash
# Frontend
cd client && npm run dev

# Backend  
cd server && python app.py
```

### Production (Vercel)
- Frontend: Automatically built and served as static files
- Backend: Runs as serverless functions
- API URL: Automatically switches via environment variables

## 📋 Deployment Checklist

- ✅ Code pushed to Git repository
- ✅ Vercel project created and connected
- ✅ Build successful
- ✅ Frontend loads at main URL
- ✅ API health check responds
- ✅ Asteroid data endpoints work
- ✅ Map functionality works
- ✅ All routes accessible

Your AstroShield application is now ready for Vercel deployment with minimal changes to your existing codebase!