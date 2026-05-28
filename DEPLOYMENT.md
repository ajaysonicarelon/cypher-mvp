# Deployment Guide

## Architecture

**Frontend:** Netlify (Static hosting)
**Backend:** Render (Python Flask API)
**Database:** Supabase (PostgreSQL)

## Files Structure

### Backend (Render)
- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `database/` - Database scripts (not deployed)

### Frontend (Netlify)
- `public/index.html` - Main UI
- `index.html` - Root HTML (same as public)

## Deployment Steps

### 1. Deploy Backend to Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo: `ajaysonicarelon/cypher-mvp`
4. Configure:
   - **Name:** `cypher-backend` (or any name)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
5. Add Environment Variables:
   - `SUPABASE_URL` = `https://hlfwxqyjvslvukkqgpvf.supabase.co`
   - `SUPABASE_KEY` = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsZnd4cXlqdnNsdnVra3FncHZmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk4OTE2NDksImV4cCI6MjA5NTQ2NzY0OX0.raD3fPzNuyf1q-zuJMvkETfcgEUXPlVvTQyuVlCsVfY`
   - `CONFIDENCE_THRESHOLD` = `0.40`
6. Click "Create Web Service"
7. Wait for deployment (~5 minutes)
8. Copy the Render URL (e.g., `https://cypher-backend.onrender.com`)

### 2. Update Frontend with Backend URL

After Render deployment, update both HTML files:

In `public/index.html` and `index.html`, replace:
```javascript
const API_ENDPOINT = ... 'RENDER_BACKEND_URL_PLACEHOLDER/chat';
```

With:
```javascript
const API_ENDPOINT = ... 'https://YOUR-RENDER-URL.onrender.com/chat';
```

### 3. Deploy Frontend to Netlify

Frontend is already deployed at: `https://uxcypher.netlify.app`

After updating the backend URL:
1. Commit and push changes
2. Netlify will auto-deploy
3. Test the chatbot!

## Testing

1. **Backend Health Check:**
   ```
   curl https://YOUR-RENDER-URL.onrender.com/health
   ```

2. **Frontend:**
   Open `https://uxcypher.netlify.app` and send a message

## Logs

- **Render Logs:** Dashboard → Your Service → Logs
- **Netlify Logs:** Dashboard → Site → Deploys
- **Browser Console:** F12 → Console tab
