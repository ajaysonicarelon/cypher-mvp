# Cypher Chatbot - Deployment Guide

## Overview

This guide covers deploying the complete Cypher chatbot system:
- Backend API (Flask) → Render
- Admin Dashboard (React) → Netlify
- Widget SDK → CDN
- Database → Supabase

## Prerequisites

- GitHub account
- Render account (free tier)
- Netlify account (free tier)
- Supabase account (free tier)
- Domain for widget hosting (optional)

## Step 1: Deploy Database (Supabase)

1. **Create Supabase Project**
   - Go to https://supabase.com
   - Create a new project
   - Note your project URL and anon key

2. **Run Database Schema**
   - Go to SQL Editor in Supabase
   - Open `database/multi_tenant_schema.sql`
   - Execute the SQL script
   - This creates tables: products, widgets, api_keys, knowledge_base, analytics

3. **Set Environment Variables**
   - Copy SUPABASE_URL and SUPABASE_KEY
   - You'll need these for Render deployment

## Step 2: Deploy Backend API (Render)

1. **Push Code to GitHub**
   ```bash
   git add .
   git commit -m "Add Cypher chatbot deployment"
   git push origin main
   ```

2. **Create Render Service**
   - Go to https://render.com
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Render will detect `render.yaml` automatically

3. **Configure Environment Variables**
   - Add `SUPABASE_URL`: your Supabase project URL
   - Add `SUPABASE_KEY`: your Supabase anon key
   - Add `FLASK_ENV`: `production`

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy
   - Note the API URL (e.g., `https://cypher-api.onrender.com`)

## Step 3: Deploy Admin Dashboard (Netlify)

1. **Build Frontend** (already done)
   ```bash
   cd frontend
   npm run build
   ```
   - Build files are in `frontend/build/`

2. **Deploy to Netlify**
   - Go to https://netlify.com
   - Click "Add new site" → "Deploy manually"
   - Drag and drop the `frontend/build` folder
   - Or connect GitHub repository (recommended)
   - Netlify will detect `netlify.toml` automatically

3. **Configure Environment Variables** (if needed)
   - Add `REACT_APP_API_ENDPOINT`: your Render API URL
   - Example: `https://cypher-api.onrender.com`

4. **Deploy**
   - Click "Deploy site"
   - Note the admin dashboard URL

## Step 4: Host Widget SDK (CDN)

### Option A: Netlify (Recommended)
1. Create a new Netlify site
2. Upload `cypher-widget-sdk/dist/` folder
3. Get the CDN URL
4. Update `INTEGRATION_GUIDE.md` with the URL

### Option B: Cloudflare R2
1. Create R2 bucket
2. Upload widget files
3. Enable public access
4. Get CDN URL
5. Update integration guide

### Option C: GitHub Pages
1. Create separate repo for widget
2. Push `cypher-widget-sdk/dist/` files
3. Enable GitHub Pages
4. Get URL
5. Update integration guide

## Step 5: Configure Admin Dashboard

1. **Access Admin Dashboard**
   - Open your Netlify URL
   - Click "Admin Dashboard" in sidebar

2. **Add Your Product**
   - Click "Add Product"
   - Enter product name (e.g., "My Website")
   - Enter domain (e.g., "mywebsite.com")
   - Save

3. **Create Widget**
   - Click "Widgets" tab
   - Click "Add Widget"
   - Enter widget name
   - Select your product
   - Click "Generate" for API key
   - Save
   - Copy the API key

4. **Add Knowledge Base**
   - Click "Knowledge Base" tab
   - Click "Add Q&A"
   - Add questions and answers for your product
   - Save

## Step 6: Integrate Widget into Your Website

1. **Add Widget Script**
   ```html
   <script src="https://your-cdn-url.com/cypher-widget.umd.js"></script>
   ```

2. **Initialize Widget**
   ```html
   <script>
     Cypher.init({
       apiKey: 'your-generated-api-key',
       widgetId: 'your-widget-id',
       theme: {
         primaryColor: '#5009B5',
         position: 'bottom-right'
       }
     });
   </script>
   ```

3. **Test Integration**
   - Open your website
   - Widget should appear in bottom-right corner
   - Test chat functionality
   - Verify responses match your knowledge base

## Step 7: Update Backend API URL

Update `app.py` to use production API URL for CORS:

```python
CORS(app(), resources={r"/*": {"origins": ["https://your-website.com"]}})
```

## Environment Variables Summary

### Supabase
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key

### Render (Backend)
- `SUPABASE_URL`: From Supabase
- `SUPABASE_KEY`: From Supabase
- `FLASK_ENV`: `production`

### Netlify (Frontend)
- `REACT_APP_API_ENDPOINT`: Your Render API URL

## Troubleshooting

### Backend Not Deploying
- Check Render logs
- Verify environment variables
- Ensure `requirements.txt` is present

### Frontend Not Deploying
- Check Netlify logs
- Verify build succeeded
- Check `netlify.toml` configuration

### Widget Not Loading
- Verify CDN URL is correct
- Check browser console for errors
- Ensure API key is valid

### API Key Errors
- Verify API key in admin dashboard
- Check backend is running
- Verify CORS settings

## Monitoring

### Render
- Monitor API logs in Render dashboard
- Check response times
- Monitor error rates

### Netlify
- Monitor site performance
- Check build logs
- Monitor bandwidth usage

### Supabase
- Monitor database queries
- Check storage usage
- Monitor API calls

## Next Steps

1. Set up analytics dashboard
2. Add authentication to admin dashboard
3. Implement theme builder for widget customization
4. Add webhook notifications for new messages
5. Set up automated backups

## Support

For deployment issues:
- Render: https://render.com/support
- Netlify: https://netlify.com/support
- Supabase: https://supabase.com/support
