# 🎓 Student Portal - Academic Management System

[![Django](https://img.shields.io/badge/Django-5.2.8-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14.0-red.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive academic management system with Django backend and RESTful API for web and mobile applications.

## ✨ Features

### 👨‍🎓 Students
- View enrolled courses and available courses
- Track grades with automatic GPA/CGPA calculation
- Submit and manage course reviews
- Monitor academic progress

### 👨‍🏫 Lecturers
- Manage assigned courses
- Enter and update student grades
- View course reviews and feedback
- Track student enrollment

### 👨‍💼 Administrators
- Complete system management
- User and course administration
- Generate comprehensive reports
- CSV export with automatic Supabase backup

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip
- Virtual environment (recommended)
- PostgreSQL (for production)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/SSESA-MATT/Students-portal.git
cd Portal-master
```

2. **Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Replace settings file**
```bash
# Backup old settings
cp studetPortals/settings.py studetPortals/settings_backup.py

# Use new API-enabled settings
cp studetPortals/settings_new.py studetPortals/settings.py
```

6. **Update CourseReview model**

Add `created_at` field to `reports/models.py`:
```python
class CourseReview(models.Model):
    # ... existing fields ...
    created_at = models.DateTimeField(auto_now_add=True)  # ADD THIS
```

7. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

8. **Create superuser**
```bash
python manage.py createsuperuser
```

9. **Run development server**
```bash
python manage.py runserver
```

Visit: http://localhost:8000

## 📡 API Documentation

### API Base URL
```
http://localhost:8000/api/
```

### Authentication
The API uses JWT (JSON Web Token) authentication.

**Get Token:**
```bash
POST /api/auth/login/
{
  "username": "your_username",
  "password": "your_password"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Use Token:**
```
Authorization: Bearer <access_token>
```

### API Endpoints

#### Students
- `GET /api/students/` - List students
- `GET /api/students/me/` - Current student profile
- `GET /api/students/{id}/` - Student details
- `POST /api/students/{id}/enroll/` - Enroll in course
- `POST /api/students/{id}/unenroll/` - Unenroll from course
- `GET /api/students/{id}/grades/` - Student grades
- `GET /api/students/{id}/gpa/` - GPA/CGPA

#### Courses
- `GET /api/courses/` - List courses
- `GET /api/courses/{id}/` - Course details
- `GET /api/courses/{id}/students/` - Enrolled students
- `GET /api/courses/{id}/reviews/` - Course reviews
- `POST /api/courses/` - Create course (lecturer/admin)

#### Grades
- `GET /api/grades/` - List grades
- `POST /api/grades/` - Create grade (lecturer/admin)
- `PUT /api/grades/{id}/` - Update grade (lecturer/admin)

#### Reviews
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Submit review (student)
- `PUT /api/reviews/{id}/` - Update review
- `DELETE /api/reviews/{id}/` - Delete review

### Interactive API Documentation
- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🐳 Docker Deployment

### Using Docker Compose

1. **Build and run**
```bash
docker-compose up -d --build
```

2. **Run migrations**
```bash
docker-compose exec web python manage.py migrate
```

3. **Create superuser**
```bash
docker-compose exec web python manage.py createsuperuser
```

4. **View logs**
```bash
docker-compose logs -f web
```

## ☁️ Production Deployment

### Railway (Recommended)

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login and initialize**
```bash
railway login
railway init
```

3. **Add PostgreSQL**
```bash
railway add postgresql
```

4. **Set environment variables**
```bash
railway variables set SECRET_KEY=your-secret-key
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=your-domain.com
```

5. **Deploy**
```bash
railway up
```

### Heroku

1. **Install Heroku CLI**

2. **Create app**
```bash
heroku create your-app-name
```

3. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:mini
```

4. **Set environment variables**
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
```

5. **Deploy**
```bash
git push heroku master
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## 📱 Mobile App Development

### React Native (Recommended)

See [MOBILE_APP_GUIDE.md](MOBILE_APP_GUIDE.md) for complete mobile app setup.

**Quick Start:**
```bash
npx create-expo-app StudentPortalApp
cd StudentPortalApp
npm install axios @react-navigation/native
```

**API Client Example:**
```javascript
import axios from 'axios';

const API_URL = 'http://your-backend-url/api';

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
  return response.data;
};

// Get current student
export const getCurrentStudent = async (token) => {
  const response = await api.get('/students/me/', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📊 Database Schema

### Core Models
- **Student**: User profile with GPA tracking
- **Course**: Course information and enrollment
- **Grade**: Student grades with automatic letter grading
- **CourseReview**: Course feedback and ratings
- **Profile**: User roles (Student/Lecturer/Admin)

### Relationships
- Students ↔ Courses (Many-to-Many)
- Students ↔ Grades ↔ Courses
- Students ↔ Reviews ↔ Courses

## 🔒 Security

- JWT authentication with refresh tokens
- Role-based access control
- CORS configured for mobile apps
- Environment variable for sensitive data
- CSRF protection for web forms
- SQL injection protection (Django ORM)
- XSS protection enabled

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **SSESA-MATT** - [GitHub](https://github.com/SSESA-MATT)

## 🙏 Acknowledgments

- Django REST Framework
- Supabase for backup storage
- All contributors and testers

## 📞 Support

For support, email your-email@example.com or create an issue in the repository.

## 🗺️ Roadmap

- [x] REST API implementation
- [x] JWT authentication
- [x] API documentation
- [ ] Mobile app (React Native)
- [ ] Real-time notifications
- [ ] Assignment submission system
- [ ] Attendance tracking
- [ ] Parent portal
- [ ] Analytics dashboard

---

**Made with ❤️ for education**
