# 🚀 Deploying Crystal Scraper to Render

## Overview
This guide will help you deploy both the Flask backend API and React frontend to Render.

## Prerequisites
- GitHub account with your code pushed to a repository
- Render account (sign up at https://render.com)
- Your `.env` file with API keys (GOOGLE_API_KEY or TOGETHER_API_KEY)

## Deployment Steps

### Option 1: Deploy Using render.yaml (Recommended)

1. **Push your code to GitHub** (Already done! ✅)

2. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click "New +" → "Blueprint"

3. **Connect Repository**
   - Connect your GitHub account
   - Select your repository: `sidheresearch/scrapper`
   - Render will automatically detect the `render.yaml` file

4. **Configure Environment Variables (Backend)**
   - Add your API keys:
     - `GOOGLE_API_KEY` = your-google-api-key
     - `TOGETHER_API_KEY` = your-together-api-key (if using Together AI)

5. **Deploy**
   - Click "Apply" to deploy both services
   - Wait for deployment to complete (5-10 minutes)

### Option 2: Manual Deployment

#### Deploy Backend (Flask API)

1. **Create Web Service**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Backend Service**
   - **Name**: `crystal-scraper-api`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api:app`
   - **Plan**: Free

3. **Add Environment Variables**
   - `PYTHON_VERSION` = `3.11.0`
   - `GOOGLE_API_KEY` = your-google-api-key
   - `TOGETHER_API_KEY` = your-together-api-key (optional)

4. **Deploy Backend**
   - Click "Create Web Service"
   - Note the backend URL (e.g., `https://crystal-scraper-api.onrender.com`)

#### Deploy Frontend (React App)

1. **Create Static Site or Web Service**
   - Click "New +" → "Web Service"
   - Connect the same repository

2. **Configure Frontend Service**
   - **Name**: `crystal-scraper-frontend`
   - **Environment**: Node
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npx serve -s build -l $PORT`
   - **Plan**: Free

3. **Add Environment Variables**
   - `NODE_VERSION` = `18.17.0`
   - `REACT_APP_API_URL` = `https://crystal-scraper-api.onrender.com`

4. **Deploy Frontend**
   - Click "Create Web Service"

## Update Frontend API Configuration

After deploying the backend, update your frontend to use the production API URL:

1. **Update `frontend/src/services/api.js`**:
   ```javascript
   const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
   ```

2. **Update CORS in `api.py`** to allow your frontend domain:
   ```python
   CORS(app, resources={
       r"/api/*": {
           "origins": [
               "http://localhost:3000",
               "https://crystal-scraper-frontend.onrender.com",
               "https://your-custom-domain.com"
           ],
           ...
       }
   })
   ```

## Important Notes

### Free Tier Limitations
- **Spin down after inactivity**: Free services sleep after 15 minutes of inactivity
- **First request**: May take 30-60 seconds to wake up
- **Build time**: Limited to 500 build minutes/month

### Environment Variables Required
Make sure to set these in Render:
- `GOOGLE_API_KEY` - Required for AI content formatting
- `TOGETHER_API_KEY` - Optional alternative to Google AI

### Performance Tips
1. **Keep services warm**: Use UptimeRobot or similar to ping your services every 14 minutes
2. **Optimize build**: The build process is included in your 500 build minutes
3. **Database**: If you add a database later, use Render's PostgreSQL

## Troubleshooting

### Backend Issues
- **Check logs**: View logs in Render Dashboard
- **Environment variables**: Ensure all API keys are set
- **Build failures**: Check Python version compatibility

### Frontend Issues
- **API connection**: Verify `REACT_APP_API_URL` is set correctly
- **CORS errors**: Update allowed origins in `api.py`
- **Build failures**: Check Node version and dependencies

### Common Errors
1. **"Module not found"**: Run `pip install -r requirements.txt` locally first
2. **"Port already in use"**: Render manages ports automatically
3. **"API not responding"**: Backend might be sleeping (free tier)

## URLs After Deployment
- **Backend API**: `https://crystal-scraper-api.onrender.com`
- **Frontend**: `https://crystal-scraper-frontend.onrender.com`
- **API Health Check**: `https://crystal-scraper-api.onrender.com/api/health`

## Next Steps
1. Test the deployed application
2. Set up custom domain (optional)
3. Configure monitoring with UptimeRobot
4. Set up continuous deployment (auto-deploy on git push)

## Support
For issues, check:
- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Project README: See README.md in this repository
