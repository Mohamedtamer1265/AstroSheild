# AstroShield Railway Deployment Guide

## Quick Deploy to Railway

### Option 1: Deploy from GitHub
1. Fork this repository to your GitHub account
2. Go to [Railway](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your forked `AstroSheild` repository
5. Railway will automatically detect and deploy your app

### Option 2: Deploy with Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize and deploy
railway login
railway init
railway up
```

## Environment Variables

Set these environment variables in your Railway dashboard:

### Required Variables
- `RAILWAY_ENVIRONMENT=production` (automatically set by Railway)
- `PORT` (automatically set by Railway)

### Optional Variables
- `SECRET_KEY=your-secret-key-here` (for Flask sessions)
- `FRONTEND_URL=https://your-app.railway.app` (if deploying frontend separately)

### React Environment Variables (if needed)
- `REACT_APP_API_URL` (will be set to same domain in production)

## Deployment Configuration Files

The following files have been created for Railway deployment:

### `railway.json`
- Configures Railway deployment settings
- Sets health check endpoint
- Configures restart policy

### `nixpacks.toml`
- Specifies build phases
- Installs Python and Node.js dependencies
- Builds React frontend
- Configures start command

### `Procfile`
- Backup process configuration
- Specifies web server start command

### `package.json` (root)
- Full-stack build scripts
- Node.js and Python engine requirements
- Project metadata

## Project Structure for Deployment

```
AstroSheild/
├── client/                 # React frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env.production
├── server/                 # Flask backend
│   ├── app.py             # Main Flask application
│   ├── run.py             # Production server runner
│   ├── requirements.txt   # Python dependencies
│   └── controllers/       # API controllers
├── railway.json           # Railway configuration
├── nixpacks.toml          # Build configuration
├── Procfile               # Process configuration
└── package.json           # Root package.json
```

## Build Process

1. **Setup Phase**: Install Python 3.10 and Node.js 18
2. **Install Phase**: 
   - Install Python dependencies: `pip install -r server/requirements.txt`
   - Install Node.js dependencies: `cd client && npm ci`
3. **Build Phase**: Build React frontend: `cd client && npm run build`
4. **Start Phase**: Run Flask server: `python server/run.py`

## Production Features

### Backend (Flask)
- ✅ Environment-based configuration
- ✅ Production CORS settings
- ✅ Serves React build files
- ✅ Health check endpoint (`/api/health`)
- ✅ API documentation (`/api/info`)
- ✅ Error handling and logging

### Frontend (React)
- ✅ Production build optimization
- ✅ Environment variable configuration
- ✅ API endpoint detection
- ✅ Client-side routing support

### NASA Data Integration
- ✅ JPL Small-Body Database API
- ✅ Real-time asteroid data fetching
- ✅ Orbital mechanics calculations
- ✅ Impact prediction algorithms

## Post-Deployment Checklist

After deployment, verify these endpoints:

1. **Root URL**: `https://your-app.railway.app/`
   - Should serve the React application

2. **Health Check**: `https://your-app.railway.app/api/health`
   - Should return JSON with success status

3. **API Info**: `https://your-app.railway.app/api/info`
   - Should return comprehensive API documentation

4. **Asteroid Data**: `https://your-app.railway.app/api/asteroids/433`
   - Should return data for asteroid Eros

## Troubleshooting

### Common Issues

**Build Fails with "pip: command not found" (Exit code 127)**
This project now includes multiple deployment options:

1. **Dockerfile (Recommended)**: Railway will automatically detect and use the Dockerfile
2. **Nixpacks**: Alternative buildpack approach

If you get exit code 127:
- Railway should automatically switch to Docker build
- Check Railway logs for build progress
- Verify `requirements.txt` has no syntax errors

**Build Fails**
- Check that `client/package.json` has all required dependencies
- Verify `server/requirements.txt` is up to date
- Try switching build method in Railway settings

**App Won't Start**
- Check Railway logs for Python import errors
- Verify all environment variables are set
- Ensure port configuration is correct

**API Requests Fail**
- Check CORS configuration in `server/app.py`
- Verify API endpoints in `client/src/utils/api.js`

**Frontend Not Loading**
- Ensure React build succeeded (`client/dist` folder exists)
- Check Flask static file serving configuration

### Railway-Specific Tips

1. **Environment Variables**: Set in Railway dashboard under "Variables" tab
2. **Logs**: Monitor deployment and runtime logs in Railway dashboard
3. **Domain**: Railway provides automatic HTTPS domain
4. **Resources**: Monitor CPU and memory usage in dashboard

## Custom Domain (Optional)

To use a custom domain:
1. Go to Railway dashboard → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update `FRONTEND_URL` environment variable if needed

## Scaling

Railway automatically handles scaling based on traffic. For high-traffic scenarios:
- Monitor resource usage in dashboard
- Consider upgrading Railway plan if needed
- Optimize API endpoints for better performance

---

## Support

For deployment issues:
- Check Railway documentation: https://docs.railway.app
- Review logs in Railway dashboard
- Verify all configuration files are properly set up