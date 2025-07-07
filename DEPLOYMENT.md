# 🚀 ActuaryHub Deployment Guide

Complete guide to deploy your ActuaryHub application to production.

## 🌐 Frontend Deployment (Vercel)

### Step 1: Prepare Your Repository
```bash
# Ensure your code is in a GitHub repository
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Deploy to Vercel

#### Option A: Vercel Dashboard (Recommended)
1. Go to [vercel.com](https://vercel.com) and sign up/login
2. Click "New Project"
3. Import your GitHub repository
4. Configure settings:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

#### Option B: Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login and deploy
vercel login
vercel

# Follow prompts and deploy to production
vercel --prod
```

### Step 3: Environment Variables
In Vercel dashboard, add:
- `VITE_API_URL`: Your backend API URL (e.g., `https://your-backend.railway.app/api`)

## 🔧 Backend Deployment Options

### Option 1: Railway (Recommended)

1. **Create Railway Account**: Go to [railway.app](https://railway.app)
2. **New Project**: Click "New Project" → "Deploy from GitHub repo"
3. **Select Repository**: Choose your backend repository
4. **Add Database**: Click "New" → "Database" → "PostgreSQL"
5. **Environment Variables**:
   ```
   DATABASE_URL=postgresql://... (auto-generated)
   FLASK_ENV=production
   FLASK_DEBUG=False
   PORT=5000
   ```
6. **Deploy**: Railway auto-deploys on git push

### Option 2: Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create app
cd backend
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set FLASK_DEBUG=False

# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Option 3: DigitalOcean App Platform

1. Connect GitHub repository
2. Choose Python app
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `python app.py`
5. Add PostgreSQL database
6. Configure environment variables

## 🔗 Connect Frontend and Backend

1. **Get Backend URL**: After backend deployment, copy the URL
2. **Update Frontend**: In Vercel, set `VITE_API_URL` environment variable
3. **Update CORS**: In backend `app.py`, add your frontend domain to CORS origins:
   ```python
   CORS(app, origins=[
       "http://localhost:5173",
       "https://your-frontend.vercel.app"
   ])
   ```
4. **Redeploy**: Both frontend and backend will auto-redeploy

## 🗄️ Database Setup

### PostgreSQL (Production)
```sql
-- Your database will be auto-created by Railway/Heroku
-- Tables are created automatically by Flask-SQLAlchemy
```

### Environment Variables
```env
# Production Backend
DATABASE_URL=postgresql://username:password@host:port/database
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000

# Production Frontend
VITE_API_URL=https://your-backend-url.com/api
```

## 🔍 Testing Your Deployment

### 1. Test Backend API
```bash
# Health check
curl https://your-backend-url.com/api/health

# Get jobs
curl https://your-backend-url.com/api/jobs
```

### 2. Test Frontend
- Visit your Vercel URL
- Check browser console for errors
- Test all functionality (create, edit, delete jobs)
- Verify responsive design on mobile

### 3. Test Integration
- Ensure frontend can fetch data from backend
- Test job creation, editing, deletion
- Verify search and filtering works

## 🚀 Custom Domain (Optional)

### Vercel Custom Domain
1. In Vercel dashboard → Project Settings → Domains
2. Add your domain (e.g., `actuaryhub.com`)
3. Configure DNS records as instructed
4. SSL certificate is auto-generated

### Backend Custom Domain
- Railway: Add custom domain in project settings
- Heroku: `heroku domains:add yourdomain.com`

## 📊 Monitoring & Analytics

### Vercel Analytics
- Enable in project settings
- Monitor performance and usage

### Backend Monitoring
- Railway: Built-in metrics and logs
- Heroku: Use Heroku metrics or add-ons like New Relic

## 🔧 Troubleshooting

### Common Issues

1. **CORS Errors**
   ```python
   # Update backend CORS settings
   CORS(app, origins=["https://your-frontend-domain.vercel.app"])
   ```

2. **Environment Variables Not Loading**
   - Ensure variables are set in deployment platform
   - Redeploy after adding variables
   - Check variable names (VITE_ prefix for frontend)

3. **Database Connection Issues**
   - Verify DATABASE_URL format
   - Check database is running
   - Ensure connection limits not exceeded

4. **Build Failures**
   - Check build logs in deployment platform
   - Verify all dependencies in requirements.txt/package.json
   - Check Python/Node.js version compatibility

5. **API Not Responding**
   - Check backend deployment logs
   - Verify PORT environment variable
   - Test API endpoints directly

### Debug Commands
```bash
# Check Vercel deployment logs
vercel logs

# Check Railway logs
railway logs

# Check Heroku logs
heroku logs --tail
```

## 🎯 Production Checklist

- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Railway/Heroku
- [ ] PostgreSQL database configured
- [ ] Environment variables set
- [ ] CORS configured for production domain
- [ ] Custom domain configured (optional)
- [ ] SSL certificates active
- [ ] All functionality tested in production
- [ ] Performance monitoring enabled
- [ ] Error tracking configured

## 🔄 Continuous Deployment

### Auto-Deploy Setup
- **Vercel**: Auto-deploys on git push to main branch
- **Railway**: Auto-deploys on git push
- **Heroku**: Auto-deploys with GitHub integration

### Staging Environment
Consider setting up staging environments:
- Frontend: Deploy from `develop` branch
- Backend: Separate staging app with test database

## 📞 Support

If you encounter issues:
1. Check deployment platform documentation
2. Review application logs
3. Test API endpoints with tools like Postman
4. Verify environment variables are correct
5. Check CORS configuration

Your ActuaryHub application is now live and ready for users! 🎉

## 🌟 Post-Deployment

### Marketing Your Application
- Share on LinkedIn, actuarial forums
- Submit to job board directories
- Create social media presence
- Write blog posts about features

### Maintenance
- Monitor application performance
- Update dependencies regularly
- Backup database periodically
- Monitor user feedback and iterate

**Congratulations! Your ActuaryHub is now live on the internet!** 🚀