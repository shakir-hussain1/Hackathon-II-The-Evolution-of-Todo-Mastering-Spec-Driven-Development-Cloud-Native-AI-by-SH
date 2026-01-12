# Phase 2 Deployment Guide

Complete guide for deploying the Full-Stack Todo Application to production.

## Architecture

- **Frontend**: Next.js 16+ → Vercel
- **Backend**: FastAPI + Python 3.10+ → Render
- **Database**: PostgreSQL → Render (or Neon)

---

## Part 1: Deploy Backend to Render

### Step 1: Prepare Your Repository

1. Make sure all changes are committed to your GitHub repository:
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Create PostgreSQL Database on Render

1. Go to [render.com](https://render.com) and sign in/sign up
2. Click "New +" → "PostgreSQL"
3. Configure database:
   - **Name**: `phase2-todo-db`
   - **Database**: `todo_db`
   - **User**: `todo_user`
   - **Region**: Choose closest to you
   - **Plan**: Free
4. Click "Create Database"
5. **Save the connection details** (you'll need the "Internal Database URL")

### Step 3: Deploy FastAPI Backend

1. In Render dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `phase2-todo-backend`
   - **Region**: Same as database
   - **Branch**: `main` (or your deployment branch)
   - **Root Directory**: `phase2/backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

4. Add Environment Variables (click "Advanced" → "Add Environment Variable"):
   ```
   DATABASE_URL = [Paste Internal Database URL from Step 2]
   JWT_SECRET = [Generate a random 32+ character string]
   BETTER_AUTH_SECRET = [Generate another random 32+ character string]
   DEBUG = False
   PORT = 10000
   ```

   To generate secrets, you can use:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. Click "Create Web Service"
6. Wait for deployment to complete (5-10 minutes)
7. **Save your backend URL**: `https://phase2-todo-backend.onrender.com`

### Step 4: Verify Backend Deployment

Once deployed, test your backend:
```bash
curl https://phase2-todo-backend.onrender.com/health
```

You should see: `{"status":"ok","message":"API is running"}`

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Prepare Frontend for Deployment

The frontend is already configured and ready to deploy!

### Step 2: Deploy to Vercel

#### Option A: Using Vercel CLI (Recommended)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Navigate to frontend directory:
```bash
cd phase2/frontend
```

3. Login to Vercel:
```bash
vercel login
```

4. Deploy:
```bash
vercel
```

5. Follow the prompts:
   - **Set up and deploy**: Yes
   - **Which scope**: Your account
   - **Link to existing project**: No
   - **Project name**: phase2-todo-app
   - **Directory**: ./
   - **Override settings**: No

6. Add environment variable during deployment or after:
```bash
vercel env add NEXT_PUBLIC_API_URL production
```
Then paste your Render backend URL: `https://phase2-todo-backend.onrender.com`

7. Deploy to production:
```bash
vercel --prod
```

#### Option B: Using Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `phase2/frontend`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)
   - **Install Command**: `npm install` (default)

5. Add Environment Variables:
   - Click "Environment Variables"
   - Add:
     ```
     NEXT_PUBLIC_API_URL = https://phase2-todo-backend.onrender.com
     ```

6. Click "Deploy"
7. Wait for deployment (2-5 minutes)
8. **Save your frontend URL**: `https://phase2-todo-app.vercel.app`

### Step 3: Verify Frontend Deployment

1. Open your Vercel URL in a browser
2. Try signing up with a new account
3. Create a todo task
4. Verify tasks are saved and displayed correctly

---

## Part 3: Post-Deployment Configuration

### Update CORS (if needed)

If you want to restrict CORS to only your Vercel domain, update `phase2/backend/src/middleware/auth.py`:

```python
# Line 91
cors_headers = {
    "Access-Control-Allow-Origin": "https://phase2-todo-app.vercel.app",  # Your Vercel URL
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept",
}
```

Then redeploy backend:
```bash
git add .
git commit -m "Update CORS for production"
git push origin main
```

Render will automatically redeploy.

### Custom Domain (Optional)

#### For Vercel (Frontend):
1. Go to your project settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

#### For Render (Backend):
1. Go to your service settings → Custom Domains
2. Add your custom domain (requires paid plan)
3. Update DNS records as instructed

---

## Environment Variables Summary

### Backend (Render)
```env
DATABASE_URL=postgresql://user:pass@host/db  # From Render PostgreSQL
JWT_SECRET=your-generated-secret-32-chars
BETTER_AUTH_SECRET=your-generated-secret-32-chars
DEBUG=False
PORT=10000
```

### Frontend (Vercel)
```env
NEXT_PUBLIC_API_URL=https://phase2-todo-backend.onrender.com
```

---

## Troubleshooting

### Backend Issues

**Database Connection Errors:**
- Verify DATABASE_URL is the "Internal Database URL" from Render
- Check that database and backend are in the same region

**CORS Errors:**
- Verify CORS middleware is allowing your Vercel domain
- Check browser console for specific error messages

**500 Errors:**
- Check Render logs: Dashboard → Your Service → Logs
- Look for Python errors or missing environment variables

### Frontend Issues

**API Connection Errors:**
- Verify NEXT_PUBLIC_API_URL is set correctly in Vercel
- Test backend health endpoint: `curl https://your-backend.onrender.com/health`

**Build Errors:**
- Check Vercel deployment logs
- Verify all dependencies are in package.json

**Authentication Issues:**
- Check browser console for JWT errors
- Verify backend JWT_SECRET is set correctly

---

## Monitoring & Maintenance

### Render (Backend)
- **Logs**: Dashboard → Service → Logs
- **Metrics**: Dashboard → Service → Metrics
- **Free Tier**: Sleeps after 15 minutes of inactivity (takes 30s to wake up)

### Vercel (Frontend)
- **Logs**: Dashboard → Project → Deployments → Logs
- **Analytics**: Dashboard → Project → Analytics
- **Free Tier**: Unlimited deployments, 100GB bandwidth/month

---

## CI/CD (Automatic Deployments)

Both Render and Vercel support automatic deployments:

### Render
- Auto-deploys on every push to `main` branch
- Configure in: Dashboard → Service → Settings → Build & Deploy

### Vercel
- Auto-deploys on every push to `main` branch
- Preview deployments for pull requests
- Configure in: Dashboard → Project → Settings → Git

---

## Security Checklist

Before going live:
- [ ] Change all default secrets (JWT_SECRET, BETTER_AUTH_SECRET)
- [ ] Use strong, unique secrets (32+ characters)
- [ ] Never commit .env files to Git
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS (automatic on Render & Vercel)
- [ ] Set DEBUG=False in production
- [ ] Review CORS settings (restrict to your domain)
- [ ] Monitor logs for suspicious activity

---

## Cost Breakdown

### Free Tier Limits

**Render Free Tier:**
- 750 hours/month (enough for 1 service running 24/7)
- 512 MB RAM
- Sleeps after 15 minutes of inactivity
- PostgreSQL: 1GB storage, expires after 90 days

**Vercel Free Tier:**
- Unlimited deployments
- 100GB bandwidth/month
- 6000 build minutes/month
- Automatic HTTPS & CDN

### Upgrade Paths

If you need more:
- **Render Starter**: $7/month (always-on, 512MB RAM)
- **Vercel Pro**: $20/month (unlimited bandwidth, advanced analytics)

---

## Next Steps

1. Deploy backend to Render ✅
2. Deploy frontend to Vercel ✅
3. Test end-to-end flow
4. Set up custom domain (optional)
5. Enable monitoring & alerts
6. Share your app with users! 🚀

---

**Questions or Issues?**
Check the troubleshooting section or create an issue in your GitHub repository.
