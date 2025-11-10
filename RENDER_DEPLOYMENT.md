# 🚀 Render Deployment Guide

## Prerequisites
- GitHub account with your code pushed
- Render account (free tier available at https://render.com)
- Supabase account for file storage (already configured)

## Step 1: Prepare Your Repository

### 1.1 Update Configuration Files
```bash
cd /c/Users/Trinity/Portal-master/Portal-master

# Copy new settings and URLs (build.sh will do this automatically)
cp studetPortals/settings_new.py studetPortals/settings.py
cp studetPortals/urls_new.py studetPortals/urls.py
```

### 1.2 Commit and Push to GitHub
```bash
git add .
git commit -m "Add REST API, Render deployment config, and mobile app support"
git push origin master
```

## Step 2: Deploy to Render

### 2.1 Create New Web Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `SSESA-MATT/Students-portal`
4. Configure the service:

**Basic Settings:**
- **Name**: `student-portal-api`
- **Region**: Choose closest to your users
- **Branch**: `master`
- **Root Directory**: `Portal-master` (if your repo has the nested structure)
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn studetPortals.wsgi:application --bind 0.0.0.0:$PORT`

**Instance Type:**
- Free tier or Starter ($7/month recommended for production)

### 2.2 Add PostgreSQL Database

1. In Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure database:
   - **Name**: `student-portal-db`
   - **Database**: `studentportal`
   - **User**: `studentportal`
   - **Region**: Same as web service
   - **Plan**: Free or Starter

3. Click **"Create Database"**
4. Copy the **Internal Database URL** (starts with `postgresql://`)

### 2.3 Configure Environment Variables

In your web service settings, add these environment variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate a new one: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `student-portal-api.onrender.com,your-custom-domain.com` (use your actual Render URL) |
| `DATABASE_URL` | Paste the Internal Database URL from Step 2.2 |
| `SUPABASE_URL` | `https://jyifbkgzfgfdpnqorwzw.supabase.co` (or your Supabase URL) |
| `SUPABASE_KEY` | Your Supabase anon key |
| `SUPABASE_BUCKET_NAME` | `reports` |
| `CORS_ALLOWED_ORIGINS` | `https://your-mobile-app.com,http://localhost:19000` |

### 2.4 Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repo
   - Run `build.sh` (install deps, run migrations)
   - Start gunicorn server
3. Monitor deployment logs
4. Once deployed, your API will be at: `https://student-portal-api.onrender.com`

## Step 3: Create Superuser

After first deployment, create an admin user:

1. Go to your web service in Render Dashboard
2. Click **"Shell"** tab
3. Run:
```bash
python manage.py createsuperuser
```

Follow prompts to create username/password.

## Step 4: Test Your Deployment

### 4.1 Test API Documentation
Visit: `https://student-portal-api.onrender.com/api/schema/swagger-ui/`

### 4.2 Test Admin Panel
Visit: `https://student-portal-api.onrender.com/admin/`
Login with superuser credentials.

### 4.3 Test JWT Authentication
```bash
curl -X POST https://student-portal-api.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Should return:
```json
{
  "access": "eyJ0eXAiOiJKV1Qi...",
  "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

### 4.4 Test API Endpoint
```bash
curl https://student-portal-api.onrender.com/api/students/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Step 5: Configure Custom Domain (Optional)

1. In Render Dashboard → Your Web Service → Settings
2. Scroll to **"Custom Domain"**
3. Click **"Add Custom Domain"**
4. Enter your domain (e.g., `api.yourdomain.com`)
5. Update your domain's DNS:
   - Add CNAME record pointing to your Render URL
6. Render will automatically provision SSL certificate

## Render-Specific Settings

### Auto-Deploy on Push
- By default, Render auto-deploys on every push to `master`
- Disable in Settings → Build & Deploy → Auto-Deploy

### Health Check Endpoint
Add to `studetPortals/urls.py`:
```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "healthy"})

urlpatterns = [
    # ... existing patterns
    path('health/', health_check, name='health'),
]
```

### Background Workers (Optional)
For async tasks (email, notifications):
1. Create `worker.py` with Celery config
2. Add Background Worker in Render
3. Use Redis for queue

### Cron Jobs (Optional)
For scheduled tasks:
1. In Render Dashboard → Cron Jobs
2. Add new cron job
3. Command: `python manage.py your_command`
4. Schedule: Use cron syntax

## Troubleshooting

### Build Fails
- Check build logs in Render Dashboard
- Ensure `build.sh` is executable: `chmod +x build.sh`
- Verify all dependencies in `requirements.txt`

### Migration Errors
- Check if database is connected
- Run migrations manually in Shell:
  ```bash
  python manage.py migrate --run-syncdb
  ```

### Static Files Not Loading
- Ensure `collectstatic` runs in `build.sh`
- Verify `STATIC_ROOT` in settings
- Use WhiteNoise for static file serving (already in `settings_new.py`)

### CORS Errors
- Update `CORS_ALLOWED_ORIGINS` with your mobile app URL
- Check mobile app is sending requests to correct API URL

### Database Connection Issues
- Verify `DATABASE_URL` is set correctly
- Use Internal Database URL (not External)
- Check database is in same region as web service

## Monitoring & Logs

### View Logs
1. Render Dashboard → Your Web Service
2. Click **"Logs"** tab
3. Real-time logs show all requests and errors

### Metrics
1. Click **"Metrics"** tab
2. View CPU, Memory, Response times
3. Set up alerts for downtime

### Error Tracking (Recommended)
Add Sentry for error monitoring:
```bash
pip install sentry-sdk
```

In `settings.py`:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

## Cost Estimation

### Free Tier
- Web Service: Free (spins down after 15 min inactivity)
- PostgreSQL: Free (expires after 90 days, 1GB storage)
- **Total: $0/month**

### Starter Plan (Recommended for Production)
- Web Service: $7/month (always on, 512MB RAM)
- PostgreSQL: $7/month (no expiration, 1GB storage)
- **Total: $14/month**

### Pro Plan
- Web Service: $25/month (2GB RAM, autoscaling)
- PostgreSQL: $20/month (4GB storage, backups)
- **Total: $45/month**

## Update & Redeploy

### Manual Redeploy
1. Render Dashboard → Your Web Service
2. Click **"Manual Deploy"** → Deploy latest commit

### Automatic Redeploy
- Just push to `master` branch
- Render will automatically rebuild and deploy

### Rollback
1. Render Dashboard → Your Web Service → Events
2. Find previous successful deploy
3. Click **"Rollback"**

## Environment-Specific URLs

### Development (Local)
- API: `http://localhost:8000/api/`
- Admin: `http://localhost:8000/admin/`
- Swagger: `http://localhost:8000/api/schema/swagger-ui/`

### Production (Render)
- API: `https://student-portal-api.onrender.com/api/`
- Admin: `https://student-portal-api.onrender.com/admin/`
- Swagger: `https://student-portal-api.onrender.com/api/schema/swagger-ui/`

## Next Steps

✅ Backend deployed to Render
✅ PostgreSQL database configured
✅ API endpoints accessible
✅ Swagger documentation live

Now ready to:
1. **Test all API endpoints** via Swagger UI
2. **Create test data** via admin panel
3. **Build mobile app** that consumes this API
4. **Monitor and scale** as users grow

---

**Your API is LIVE! 🎉**

Base URL: `https://student-portal-api.onrender.com`

Share this with your mobile app developers!
