# 🚀 Vercel Deployment Guide

Complete guide to deploying your AI Chatbot to Vercel.

---

## 📋 Prerequisites

- ✅ Supabase database set up (Phase 1 complete)
- ✅ GitHub account
- ✅ Vercel account (free tier is perfect)
- ✅ Your code pushed to GitHub

---

## 🎯 Quick Deploy (5 Minutes)

### Step 1: Push to GitHub

```bash
cd /Users/AM07832/CascadeProjects/cypher/mvp

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AI Chatbot with Supabase"

# Create GitHub repo and push
# (Follow GitHub instructions to add remote and push)
```

### Step 2: Connect to Vercel

1. Go to https://vercel.com
2. Sign up / Log in (use GitHub)
3. Click **"Add New Project"**
4. **Import** your GitHub repository
5. Vercel will auto-detect the configuration!

### Step 3: Configure Environment Variables

In Vercel project settings, add these environment variables:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
CONFIDENCE_THRESHOLD=0.40
```

**How to add:**
1. Go to Project Settings
2. Click "Environment Variables"
3. Add each variable
4. Click "Save"

### Step 4: Deploy!

Click **"Deploy"** and wait ~2 minutes.

Your chatbot will be live at: `https://your-project.vercel.app`

---

## 📂 Project Structure for Vercel

```
mvp/
├── api/                    # Serverless functions
│   ├── chat.py            # Chat endpoint
│   └── health.py          # Health check
├── public/                # Static files
│   └── index.html         # Frontend
├── vercel.json            # Vercel configuration
├── requirements.txt       # Python dependencies
└── .vercelignore          # Files to ignore
```

---

## 🔧 Vercel Configuration Explained

### `vercel.json`

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/**/*.py",
      "use": "@vercel/python"      // Python serverless functions
    },
    {
      "src": "public/**",
      "use": "@vercel/static"       // Static file hosting
    }
  ],
  "routes": [
    {
      "src": "/api/chat",
      "dest": "/api/chat.py"        // Route /api/chat to chat.py
    },
    {
      "src": "/api/health",
      "dest": "/api/health.py"      // Route /api/health to health.py
    },
    {
      "src": "/(.*)",
      "dest": "/public/$1"          // Serve static files
    }
  ]
}
```

---

## 🌐 API Endpoints

Once deployed, your API will be available at:

### Chat Endpoint
```
POST https://your-project.vercel.app/api/chat

Body:
{
  "message": "What is machine learning?"
}

Response:
{
  "reply": "Machine learning is...",
  "confidence": 0.95,
  "media_url": null
}
```

### Health Check
```
GET https://your-project.vercel.app/api/health

Response:
{
  "status": "healthy",
  "environment": {
    "supabase_url_configured": true,
    "supabase_key_configured": true,
    "confidence_threshold": 0.4
  },
  "message": "AI Chatbot API is running on Vercel",
  "version": "2.0.0"
}
```

---

## 🔄 How It Works

### Local Development
```
Browser → http://localhost:8000/chat → FastAPI Server → Supabase
```

### Vercel Production
```
Browser → https://your-app.vercel.app/api/chat → Serverless Function → Supabase
```

### Key Differences

| Aspect | Local | Vercel |
|--------|-------|--------|
| **Server** | Always running | Spins up on demand |
| **Scaling** | Single instance | Auto-scales globally |
| **Cost** | Free (your machine) | Free tier: 100GB bandwidth |
| **URL** | localhost:8000 | your-app.vercel.app |
| **Deploy** | Manual restart | Git push = auto-deploy |

---

## 🚀 Serverless Benefits

### 1. Auto-Scaling
- Handles 1 user or 10,000 users
- No configuration needed
- Pay only for what you use

### 2. Global Edge Network
- Deployed to multiple regions
- Fast response times worldwide
- Automatic CDN

### 3. Zero Maintenance
- No server management
- Automatic updates
- Built-in monitoring

### 4. Free Tier Generous
- 100GB bandwidth/month
- Unlimited requests
- Perfect for personal projects

---

## 🔐 Environment Variables

### Required
```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Optional
```bash
CONFIDENCE_THRESHOLD=0.40  # Default: 0.40
```

### How to Set in Vercel

**Method 1: Web UI**
1. Project Settings → Environment Variables
2. Add each variable
3. Select "Production", "Preview", "Development"
4. Save

**Method 2: Vercel CLI**
```bash
vercel env add SUPABASE_URL
vercel env add SUPABASE_KEY
```

---

## 🧪 Testing Your Deployment

### 1. Test Health Endpoint
```bash
curl https://your-project.vercel.app/api/health
```

Should return:
```json
{
  "status": "healthy",
  "environment": {
    "supabase_url_configured": true,
    "supabase_key_configured": true
  }
}
```

### 2. Test Chat Endpoint
```bash
curl -X POST https://your-project.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is machine learning?"}'
```

Should return:
```json
{
  "reply": "Machine learning is...",
  "confidence": 0.95,
  "media_url": null
}
```

### 3. Test Frontend
Open: `https://your-project.vercel.app`

Should see the chat interface!

---

## 🐛 Troubleshooting

### Issue 1: "Environment variables not configured"

**Problem**: Forgot to add Supabase credentials

**Solution**:
1. Go to Vercel project settings
2. Environment Variables
3. Add `SUPABASE_URL` and `SUPABASE_KEY`
4. Redeploy

---

### Issue 2: "No data in knowledge base"

**Problem**: Supabase table is empty

**Solution**:
1. Go to Supabase SQL Editor
2. Run `seed_data.sql`
3. Verify data in Table Editor

---

### Issue 3: "Module not found"

**Problem**: Missing dependencies in `requirements.txt`

**Solution**:
1. Check `requirements.txt` includes:
   ```
   supabase==2.3.0
   scikit-learn==1.3.2
   numpy==1.26.3
   ```
2. Commit and push changes
3. Vercel will auto-redeploy

---

### Issue 4: "Function timeout"

**Problem**: Cold start takes too long

**Solution**: Already configured in `vercel.json`:
```json
"functions": {
  "api/**/*.py": {
    "memory": 1024,
    "maxDuration": 10
  }
}
```

If still timing out, increase `maxDuration` to 15.

---

## 📊 Monitoring

### Vercel Dashboard

View in real-time:
- Request logs
- Error rates
- Response times
- Bandwidth usage

**Access**: Project → Analytics

### Check Logs
```bash
vercel logs
```

---

## 🔄 Continuous Deployment

Every time you push to GitHub:
1. Vercel detects the push
2. Automatically builds
3. Runs tests (if configured)
4. Deploys to production
5. Updates your live site

**No manual deployment needed!**

---

## 💰 Cost Estimate

### Free Tier (Hobby)
- ✅ 100GB bandwidth/month
- ✅ Unlimited requests
- ✅ 100 hours serverless execution
- ✅ Perfect for personal projects

### Pro Tier ($20/month)
- ✅ 1TB bandwidth
- ✅ Unlimited serverless execution
- ✅ Team collaboration
- ✅ Analytics

**For this chatbot**: Free tier is more than enough!

---

## 🎯 Next Steps After Deployment

1. **Custom Domain** (Optional)
   - Add your own domain
   - Vercel provides free SSL

2. **Analytics** (Optional)
   - Enable Vercel Analytics
   - Track usage and performance

3. **Monitoring** (Optional)
   - Set up alerts
   - Monitor error rates

4. **Phase 3**: Build MCP extractors
   - Sync from Confluence
   - Sync from Figma
   - Keep knowledge base updated

---

## 📝 Deployment Checklist

Before deploying:
- [ ] Supabase database set up
- [ ] `seed_data.sql` executed
- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] Environment variables ready

After deploying:
- [ ] Test `/api/health` endpoint
- [ ] Test `/api/chat` endpoint
- [ ] Test frontend UI
- [ ] Verify Supabase connection
- [ ] Check response times

---

## 🚀 Quick Commands

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy from terminal
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs

# Check environment variables
vercel env ls
```

---

## 🎉 Success!

Once deployed, your chatbot is:
- ✅ Live on the internet
- ✅ Auto-scaling globally
- ✅ Connected to Supabase
- ✅ Zero maintenance
- ✅ Free to run!

Share your URL: `https://your-project.vercel.app` 🌐

---

**Questions?** Check Vercel docs: https://vercel.com/docs
