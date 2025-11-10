# 🚀 Student Portal - Deployment & Mobile App Plan

## 📋 Project Overview
**Student Portal** is a Django-based academic management system with three user roles:
- 👨‍🎓 **Students**: View courses, grades, GPA/CGPA, submit reviews
- 👨‍🏫 **Lecturers**: Manage courses, enter grades, view reviews
- 👨‍💼 **Admins**: Full system management, reports, user management

### Current Features
- Course enrollment and management
- Grade tracking with automatic GPA/CGPA calculation
- Course reviews and ratings
- Multi-role authentication system
- CSV export with Supabase backup
- SQLite database (development)

---

## 🎯 Deployment Strategy

### Phase 1: API Development (Week 1)
**Goal**: Build RESTful API for mobile app consumption

#### 1.1 Install Django REST Framework
```bash
pip install djangorestframework djangorestframework-simplejwt django-cors-headers drf-spectacular django-filter
```

#### 1.2 API Endpoints to Build

**Authentication**
- `POST /api/auth/login/` - JWT token login
- `POST /api/auth/refresh/` - Refresh access token
- `POST /api/auth/verify/` - Verify token validity
- `POST /api/auth/register/` - Student registration (optional)

**Students**
- `GET /api/students/` - List students (admin/lecturer)
- `GET /api/students/{id}/` - Student details
- `GET /api/students/me/` - Current student profile
- `GET /api/students/{id}/courses/` - Student's enrolled courses
- `GET /api/students/{id}/grades/` - Student's grades
- `GET /api/students/{id}/gpa/` - Student's GPA/CGPA

**Courses**
- `GET /api/courses/` - List all courses
- `GET /api/courses/{id}/` - Course details
- `POST /api/courses/{id}/enroll/` - Enroll in course
- `DELETE /api/courses/{id}/unenroll/` - Unenroll from course
- `GET /api/courses/{id}/students/` - Students in course (lecturer)
- `GET /api/courses/{id}/reviews/` - Course reviews

**Grades**
- `GET /api/grades/` - List grades (filtered by student/course)
- `POST /api/grades/` - Create grade (lecturer)
- `PUT /api/grades/{id}/` - Update grade (lecturer)

**Reviews**
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Submit review
- `PUT /api/reviews/{id}/` - Update review
- `DELETE /api/reviews/{id}/` - Delete review

**Lecturers**
- `GET /api/lecturers/` - List lecturers
- `GET /api/lecturers/me/courses/` - My courses (lecturer)

#### 1.3 API Features
- **Pagination**: 20 items per page
- **Filtering**: Filter by course, student, semester
- **Permissions**: Role-based access control
- **Documentation**: Auto-generated Swagger/OpenAPI docs
- **Versioning**: `/api/v1/` for future compatibility

---

### Phase 2: Production Configuration (Week 1-2)

#### 2.1 Environment Variables
Create `.env` file:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/studentportal

# Supabase (already configured)
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
SUPABASE_BUCKET_NAME=reports

# Cloudinary (for media files)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# CORS (for mobile app)
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourmobileapp.com

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### 2.2 Settings Structure
```
studetPortals/
├── settings/
│   ├── __init__.py
│   ├── base.py       # Common settings
│   ├── development.py # Dev settings (SQLite)
│   ├── production.py  # Prod settings (PostgreSQL)
│   └── testing.py     # Test settings
```

#### 2.3 Dependencies for Production
```txt
# Core
Django==5.2.8
gunicorn==21.2.0
psycopg2-binary==2.9.9
dj-database-url==2.1.0
python-decouple==3.8

# API
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.1
drf-spectacular==0.27.0
django-filter==23.5

# Static/Media
whitenoise==6.6.0
Pillow==10.1.0

# Supabase (already installed)
supabase==2.23.2

# Monitoring (optional)
sentry-sdk==1.40.0
```

---

### Phase 3: Deployment Options

#### Option A: Railway (Recommended - Easiest)
**Pros**: Simple, free tier, PostgreSQL included
**Steps**:
1. Connect GitHub repo
2. Add PostgreSQL service
3. Set environment variables
4. Deploy automatically on push

#### Option B: Heroku
**Pros**: Well-documented, add-ons ecosystem
**Cons**: No free tier anymore
**Files needed**:
- `Procfile`
- `runtime.txt`
- `requirements.txt`

#### Option C: DigitalOcean App Platform
**Pros**: Affordable, scalable
**Cons**: Requires more configuration

#### Option D: Docker + VPS (Advanced)
**Pros**: Full control, cheapest long-term
**Cons**: Requires DevOps knowledge
**Services**: DigitalOcean, Linode, AWS EC2

---

### Phase 4: Docker Configuration

#### 4.1 Dockerfile
```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations on startup
CMD python manage.py migrate && gunicorn studetPortals.wsgi:application --bind 0.0.0.0:8000
```

#### 4.2 docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: studentportal
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres

  web:
    build: .
    command: gunicorn studetPortals.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

volumes:
  postgres_data:
```

---

## 📱 Mobile App Development Plan

### Mobile App Options

#### Option 1: React Native with Expo (Recommended)
**Pros**:
- Cross-platform (iOS + Android)
- Fast development
- Large community
- Hot reload
- Easy deployment

**Tech Stack**:
- **Framework**: React Native + Expo
- **State Management**: Redux Toolkit / Zustand
- **API Client**: Axios / React Query
- **Navigation**: React Navigation
- **Auth**: JWT with secure storage
- **UI Library**: React Native Paper / NativeBase

**Timeline**: 6-8 weeks

#### Option 2: Flutter
**Pros**:
- Beautiful UI out of the box
- High performance
- Single codebase
- Good documentation

**Tech Stack**:
- **Framework**: Flutter
- **State Management**: Riverpod / Bloc
- **API Client**: Dio
- **Storage**: Hive / Shared Preferences

**Timeline**: 6-8 weeks

#### Option 3: Native (iOS + Android)
**Pros**:
- Best performance
- Platform-specific features
- No framework limitations

**Cons**:
- 2x development time
- 2 codebases to maintain

**Timeline**: 12-16 weeks

---

### Mobile App Features

#### MVP Features (Week 1-4)
1. **Authentication**
   - Login with email/password
   - JWT token storage
   - Auto-refresh tokens
   - Role-based navigation

2. **Student Dashboard**
   - View enrolled courses
   - Current GPA/CGPA display
   - Grade breakdown
   - Recent notifications

3. **Courses**
   - Browse available courses
   - Course details with lecturer info
   - Enroll/unenroll functionality
   - View course materials

4. **Grades**
   - Semester grade view
   - Course-wise grades
   - GPA calculation
   - Progress tracking

5. **Reviews**
   - Submit course reviews
   - View existing reviews
   - Edit/delete own reviews

#### Advanced Features (Week 5-8)
6. **Lecturer Portal**
   - Course management
   - Grade entry
   - Student list
   - Review viewing

7. **Notifications**
   - Push notifications for new grades
   - Course enrollment confirmations
   - Assignment reminders

8. **Offline Mode**
   - Cache data locally
   - Sync when online
   - Offline grade viewing

9. **Admin Panel**
   - User management
   - Course creation
   - Report generation

---

### Mobile App Architecture

```
mobile-app/
├── src/
│   ├── api/
│   │   ├── auth.ts          # Authentication API
│   │   ├── courses.ts       # Courses API
│   │   ├── grades.ts        # Grades API
│   │   └── reviews.ts       # Reviews API
│   ├── components/
│   │   ├── CourseCard.tsx
│   │   ├── GradeItem.tsx
│   │   └── ReviewForm.tsx
│   ├── screens/
│   │   ├── auth/
│   │   │   ├── LoginScreen.tsx
│   │   │   └── RegisterScreen.tsx
│   │   ├── student/
│   │   │   ├── DashboardScreen.tsx
│   │   │   ├── CoursesScreen.tsx
│   │   │   ├── GradesScreen.tsx
│   │   │   └── ReviewsScreen.tsx
│   │   └── lecturer/
│   │       ├── LecturerDashboard.tsx
│   │       └── GradeEntry.tsx
│   ├── navigation/
│   │   ├── AppNavigator.tsx
│   │   └── AuthNavigator.tsx
│   ├── store/
│   │   ├── authSlice.ts
│   │   ├── coursesSlice.ts
│   │   └── store.ts
│   ├── utils/
│   │   ├── tokenStorage.ts
│   │   ├── api.ts
│   │   └── constants.ts
│   └── App.tsx
```

---

## 🔐 Security Checklist

- [ ] Environment variables secured
- [ ] SECRET_KEY changed for production
- [ ] DEBUG=False in production
- [ ] HTTPS enabled
- [ ] CORS configured properly
- [ ] JWT tokens with short expiry
- [ ] Rate limiting on API
- [ ] SQL injection protection (Django ORM)
- [ ] XSS protection enabled
- [ ] CSRF tokens for web forms
- [ ] Password hashing (Django default)
- [ ] Input validation on all forms
- [ ] File upload restrictions
- [ ] Database backups automated
- [ ] Error logging configured
- [ ] Monitoring setup (Sentry)

---

## 📊 Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Dependencies updated
- [ ] Security audit completed
- [ ] Database migrations tested
- [ ] Static files collected
- [ ] Environment variables configured
- [ ] Domain name purchased
- [ ] SSL certificate configured

### Deployment
- [ ] GitHub repo configured
- [ ] CI/CD pipeline setup
- [ ] Database created and migrated
- [ ] Static files served correctly
- [ ] Media files storage configured
- [ ] Email service configured
- [ ] Backup strategy implemented
- [ ] Monitoring tools installed

### Post-Deployment
- [ ] Smoke tests completed
- [ ] Performance monitoring active
- [ ] Error tracking enabled
- [ ] Documentation updated
- [ ] Team trained on deployment
- [ ] Rollback plan documented

---

## 📈 Timeline Summary

| Phase | Duration | Tasks |
|-------|----------|-------|
| API Development | Week 1 | REST API, serializers, endpoints |
| Production Setup | Week 1-2 | Settings, PostgreSQL, Docker |
| Deployment | Week 2 | Railway/Heroku deployment |
| Mobile MVP | Week 3-6 | Core features (login, courses, grades) |
| Mobile Advanced | Week 7-8 | Lecturer portal, notifications |
| Testing & Launch | Week 9 | QA, bug fixes, app store submission |

**Total Timeline**: 9 weeks for complete system

---

## 💰 Cost Estimate

### Backend Hosting (Monthly)
- **Railway Free Tier**: $0 (limited)
- **Railway Pro**: $5-20
- **Heroku**: $7-25
- **DigitalOcean**: $6-12

### Database
- **Railway PostgreSQL**: Included
- **Heroku PostgreSQL**: $9+
- **Supabase**: Free tier (already using)

### Mobile App
- **Development**: DIY or $5,000-15,000 (hire)
- **App Store Fee**: $99/year (Apple)
- **Play Store Fee**: $25 one-time (Google)

### Total Estimated Cost
- **Year 1**: $200-500 (hosting + app stores)
- **Development**: DIY or outsource

---

## 🎓 Next Steps

1. **Immediate**: Install REST Framework and create API
2. **This Week**: Test API with Postman/Swagger
3. **Next Week**: Deploy to Railway/Heroku
4. **Week 3**: Start mobile app development
5. **Week 6**: Beta testing with real users
6. **Week 9**: Production launch

---

## 📚 Resources

### Documentation
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Native Docs](https://reactnative.dev/)
- [Flutter Docs](https://flutter.dev/)
- [Railway Docs](https://docs.railway.app/)

### Tutorials
- [DRF JWT Auth Tutorial](https://simpleisbetterthancomplex.com/tutorial/2018/12/19/how-to-use-jwt-authentication-with-django-rest-framework.html)
- [React Native + Django API](https://www.youtube.com/watch?v=YKYVv0gm_0o)
- [Deploy Django to Railway](https://dev.to/osahenru/deploying-django-application-to-railway-2021-1d6k)

---

**Let's build something amazing! 🚀**
