# Student Portal - API Quick Start Guide

## ✅ Setup Complete!

The REST API infrastructure has been added to your Student Portal project.

### 📦 What Was Added:

1. **API Dependencies** (in requirements.txt):
   - Django REST Framework
   - JWT Authentication (djangorestframework-simplejwt)
   - CORS Headers (for mobile app)
   - API Documentation (drf-spectacular)
   - Filtering support (django-filter)

2. **API Structure** (in reports/api/):
   - `serializers.py` - Data serialization for API
   - `views.py` - API viewsets and endpoints
   - `permissions.py` - Role-based access control
   - `urls.py` - API URL routing

3. **Configuration**:
   - New settings file: `studetPortals/settings_new.py`
   - JWT authentication configured
   - CORS enabled for mobile apps
   - Swagger/OpenAPI documentation

---

## 🚀 Next Steps:

### 1. Install Dependencies

```bash
cd /c/Users/Trinity/Portal-master/Portal-master
source venv/Scripts/activate
pip install -r requirements.txt
```

### 2. Replace Settings File

```bash
# Backup old settings
cp studetPortals/settings.py studetPortals/settings_old.py

# Use new settings
cp studetPortals/settings_new.py studetPortals/settings.py
```

### 3. Add Missing Field to Model

Edit `reports/models.py` and add `created_at` to CourseReview model:

```python
class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # ADD THIS LINE

    def __str__(self):
        return f"{self.course.name} - {self.rating} by {self.student.name}"
```

### 4. Create and Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (if not exists)

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

---

## 📡 Available API Endpoints:

### Authentication
- `POST /api/auth/login/` - Get JWT tokens (access + refresh)
- `POST /api/auth/refresh/` - Refresh access token
- `POST /api/auth/verify/` - Verify token validity

### Students
- `GET /api/students/` - List all students
- `GET /api/students/{id}/` - Get student details
- `GET /api/students/me/` - Get current student profile
- `POST /api/students/{id}/enroll/` - Enroll in course
- `POST /api/students/{id}/unenroll/` - Unenroll from course
- `GET /api/students/{id}/grades/` - Get student grades
- `GET /api/students/{id}/gpa/` - Get student GPA/CGPA

### Courses
- `GET /api/courses/` - List all courses
- `GET /api/courses/{id}/` - Get course details
- `POST /api/courses/` - Create course (lecturer/admin)
- `PUT /api/courses/{id}/` - Update course (lecturer/admin)
- `GET /api/courses/{id}/students/` - Get enrolled students
- `GET /api/courses/{id}/reviews/` - Get course reviews

### Grades
- `GET /api/grades/` - List grades
- `POST /api/grades/` - Create grade (lecturer/admin)
- `PUT /api/grades/{id}/` - Update grade (lecturer/admin)

### Reviews
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Submit review (student)
- `PUT /api/reviews/{id}/` - Update own review
- `DELETE /api/reviews/{id}/` - Delete own review

### Profiles
- `GET /api/profiles/me/` - Get current user profile
- `GET /api/profiles/` - List all profiles (admin)

---

## 🧪 Test the API:

### 1. Get JWT Token

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

### 2. Use Token in Requests

```bash
curl http://localhost:8000/api/students/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 3. View API Documentation

Visit: http://localhost:8000/api/schema/swagger-ui/

---

## 📱 Mobile App Integration:

### React Native Example:

```javascript
// API Client
import axios from 'axios';

const API_URL = 'http://YOUR_COMPUTER_IP:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Login
export const login = async (username, password) => {
  const response = await axios.post(`${API_URL}/auth/login/`, {
    username,
    password,
  });
  return response.data; // { access, refresh }
};

// Get current student
export const getCurrentStudent = async (token) => {
  const response = await api.get('/students/me/', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

// Get courses
export const getCourses = async (token) => {
  const response = await api.get('/courses/', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};
```

---

## 🔒 Security Notes:

1. **Never commit** `.env` file or `settings.py` with real secrets
2. Change `SECRET_KEY` in production
3. Set `DEBUG=False` in production
4. Use HTTPS in production
5. Configure proper `ALLOWED_HOSTS`
6. Enable CSRF protection for web forms

---

## 📚 Documentation:

- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

---

## 🎯 Ready for Mobile Development!

Your Django backend is now API-ready. You can start building:
- React Native mobile app
- Flutter mobile app
- Any client that can make HTTP requests

All authentication, permissions, and data serialization are handled! 🎉
