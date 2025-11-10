# 🚀 Quick Reference - Student Portal API

## 📦 Installation Commands

```bash
# 1. Activate virtual environment
cd /c/Users/Trinity/Portal-master/Portal-master
source venv/Scripts/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Update configuration files
cp studetPortals/settings_new.py studetPortals/settings.py
cp studetPortals/urls_new.py studetPortals/urls.py

# 4. Update model (add to CourseReview in reports/models.py)
#    created_at = models.DateTimeField(auto_now_add=True)

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

## 🌐 URLs

| Service | URL |
|---------|-----|
| Web App | http://localhost:8000/reports/ |
| Admin | http://localhost:8000/admin/ |
| API Root | http://localhost:8000/api/ |
| Swagger UI | http://localhost:8000/api/schema/swagger-ui/ |
| ReDoc | http://localhost:8000/api/schema/redoc/ |

## 🔑 API Authentication

### Get JWT Token
```bash
POST /api/auth/login/
{
  "username": "student1",
  "password": "password123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Use Token
```
Authorization: Bearer <access_token>
```

## 📡 Key API Endpoints

### Students
```
GET    /api/students/           - List students
GET    /api/students/me/        - Current student
GET    /api/students/{id}/      - Student details
POST   /api/students/{id}/enroll/   - Enroll in course
GET    /api/students/{id}/grades/   - Get grades
GET    /api/students/{id}/gpa/      - Get GPA/CGPA
```

### Courses
```
GET    /api/courses/            - List courses
GET    /api/courses/{id}/       - Course details
POST   /api/courses/            - Create course (lecturer)
GET    /api/courses/{id}/students/  - Enrolled students
GET    /api/courses/{id}/reviews/   - Course reviews
```

### Grades
```
GET    /api/grades/             - List grades
POST   /api/grades/             - Create grade (lecturer)
PUT    /api/grades/{id}/        - Update grade (lecturer)
```

### Reviews
```
GET    /api/reviews/            - List reviews
POST   /api/reviews/            - Submit review
PUT    /api/reviews/{id}/       - Update review
DELETE /api/reviews/{id}/       - Delete review
```

## 🐳 Docker Commands

```bash
# Build and run
docker-compose up -d --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web

# Stop
docker-compose down
```

## ☁️ Railway Deployment

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Add PostgreSQL
railway add postgresql

# 5. Set environment variables
railway variables set SECRET_KEY=your-key
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=*.railway.app

# 6. Deploy
railway up

# 7. Run migrations
railway run python manage.py migrate

# 8. Create superuser
railway run python manage.py createsuperuser
```

## 📱 Mobile App API Client (React Native)

```javascript
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = 'http://YOUR_IP:8000/api';

// Login
const login = async (username, password) => {
  const response = await axios.post(`${API_URL}/auth/login/`, {
    username,
    password,
  });
  await AsyncStorage.setItem('accessToken', response.data.access);
  await AsyncStorage.setItem('refreshToken', response.data.refresh);
  return response.data;
};

// API call with token
const getStudent = async () => {
  const token = await AsyncStorage.getItem('accessToken');
  const response = await axios.get(`${API_URL}/students/me/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

// Get courses
const getCourses = async () => {
  const token = await AsyncStorage.getItem('accessToken');
  const response = await axios.get(`${API_URL}/courses/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

// Enroll in course
const enrollCourse = async (studentId, courseId) => {
  const token = await AsyncStorage.getItem('accessToken');
  const response = await axios.post(
    `${API_URL}/students/${studentId}/enroll/`,
    { course_id: courseId },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data;
};

// Submit review
const submitReview = async (courseId, rating, comment) => {
  const token = await AsyncStorage.getItem('accessToken');
  const response = await axios.post(
    `${API_URL}/reviews/`,
    { course: courseId, rating, comment },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data;
};
```

## 🔧 Troubleshooting

### Can't install packages?
```bash
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

### Port already in use?
```bash
# Find process
netstat -ano | findstr :8000

# Kill process
taskkill /PID <process_id> /F

# Or use different port
python manage.py runserver 8001
```

### Mobile app can't connect?
```bash
# Find your IP
ipconfig  # Windows
ifconfig  # Mac/Linux

# Run server on all interfaces
python manage.py runserver 0.0.0.0:8000

# Update mobile app API_URL to http://YOUR_IP:8000/api
```

### CORS errors?
Add your mobile app URL to `CORS_ALLOWED_ORIGINS` in `settings.py`

## 📚 File Structure

```
Portal-master/
├── reports/                    # Main app
│   ├── api/                   # REST API
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── permissions.py
│   │   └── urls.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── studetPortals/             # Project settings
│   ├── settings.py           # Use settings_new.py
│   ├── urls.py               # Use urls_new.py
│   └── wsgi.py
├── requirements.txt           # Updated with API deps
├── Dockerfile
├── docker-compose.yml
├── Procfile                  # For Railway/Heroku
├── runtime.txt
├── .env.example
├── .gitignore
├── README.md
├── DEPLOYMENT_PLAN.md
├── API_QUICKSTART.md
└── SUMMARY.md
```

## ✅ Pre-Deployment Checklist

- [ ] SECRET_KEY changed from default
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS configured
- [ ] Database migrations run
- [ ] Static files collected
- [ ] Environment variables set
- [ ] Superuser created
- [ ] API endpoints tested
- [ ] CORS configured for mobile
- [ ] .env not committed to git

## 🎯 Success Indicators

✅ Server runs without errors
✅ Swagger UI loads at /api/schema/swagger-ui/
✅ JWT login returns tokens
✅ API endpoints return data
✅ Mobile app can authenticate
✅ Docker container runs
✅ Deployment successful

## 📞 Need Help?

- Check documentation files (README.md, DEPLOYMENT_PLAN.md, etc.)
- Review Swagger UI for API details
- Check Django error logs
- Review Docker/Railway logs
- Create GitHub issue

---

**Last Updated**: 2025-11-09
**Project**: Student Portal v1.0
**Status**: Production Ready 🚀
