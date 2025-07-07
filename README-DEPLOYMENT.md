# 🚀 Deploying ActuaryHub to Vercel

This guide will help you deploy your ActuaryHub application to Vercel.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Vercel CLI** (optional): `npm i -g vercel`

## 🎨 Frontend Deployment (This Project)

### Method 1: Vercel Dashboard (Recommended)

1. **Connect GitHub Repository**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository

2. **Configure Build Settings**:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

3. **Environment Variables**:
   - Add `VITE_API_URL` with your backend API URL
   - Example: `https://your-backend-api.vercel.app/api`

4. **Deploy**:
   - Click "Deploy"
   - Your frontend will be available at `https://your-project.vercel.app`

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project root
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - Project name: actuaryhub
# - Directory: ./
# - Override settings? N

# Set environment variables
vercel env add VITE_API_URL
# Enter: https://your-backend-api.vercel.app/api

# Deploy to production
vercel --prod
```

## 🔧 Backend Deployment

Since your backend is a Flask application, you have several options:

### Option 1: Vercel (Serverless Functions)

Create a new repository for your backend and add:

```python
# api/index.py
from backend.app import app

# Vercel expects the app to be available at the module level
application = app

if __name__ == "__main__":
    app.run()
```

```json
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### Option 2: Railway (Recommended for Flask)

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository (backend folder)
3. Add environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `FLASK_ENV`: production
4. Railway will auto-deploy your Flask app

### Option 3: Heroku

```bash
# Install Heroku CLI
# Create Procfile in backend directory
echo "web: python app.py" > backend/Procfile

# Deploy to Heroku
cd backend
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## 🔗 Connecting Frontend and Backend

1. **Deploy Backend First**: Get your backend URL
2. **Update Frontend Environment**:
   ```bash
   # In Vercel dashboard, add environment variable:
   VITE_API_URL=https://your-backend-url.com/api
   ```
3. **Redeploy Frontend**: Vercel will automatically redeploy

## 🌐 Custom Domain (Optional)

1. **In Vercel Dashboard**:
   - Go to your project settings
   - Click "Domains"
   - Add your custom domain
   - Follow DNS configuration instructions

## 🔧 Environment Variables

### Frontend (.env)
```env
VITE_API_URL=https://your-backend-api.vercel.app/api
```

### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@host:port/database
FLASK_ENV=production
FLASK_DEBUG=False
```

## 🚀 Deployment Checklist

- [ ] Backend deployed and accessible
- [ ] Database configured (PostgreSQL recommended)
- [ ] Frontend environment variables set
- [ ] CORS configured in backend for frontend domain
- [ ] Frontend deployed to Vercel
- [ ] Test all functionality in production
- [ ] Custom domain configured (optional)

## 🔍 Troubleshooting

### Common Issues:

1. **CORS Errors**:
   ```python
   # In backend/app.py, update CORS configuration:
   CORS(app, origins=["https://your-frontend-domain.vercel.app"])
   ```

2. **Environment Variables Not Loading**:
   - Ensure variables start with `VITE_` for frontend
   - Redeploy after adding environment variables

3. **Build Failures**:
   - Check build logs in Vercel dashboard
   - Ensure all dependencies are in package.json
   - Verify Node.js version compatibility

4. **API Connection Issues**:
   - Verify backend URL is correct
   - Check network tab in browser dev tools
   - Ensure backend is deployed and accessible

## 📞 Support

If you encounter issues:
1. Check Vercel deployment logs
2. Verify environment variables
3. Test API endpoints directly
4. Check browser console for errors

Your ActuaryHub application will be live and accessible worldwide! 🎉