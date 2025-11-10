# Django Student Portal

A comprehensive student management system built with Django 5.2.8, featuring course management, grade tracking, student reports, and Supabase integration for cloud storage.

## Features

- 👥 **User Management**: Students, Lecturers, and Admin roles
- 📚 **Course Management**: Create, edit, and manage courses
- 📊 **Grade Tracking**: Record and view student grades with GPA calculation
- 📝 **Course Reviews**: Students can submit reviews for courses
- 📄 **Student Reports**: Generate comprehensive student academic reports
- ☁️ **Cloud Storage**: Supabase integration for file storage

## Prerequisites

- Python 3.11+
- pip (Python package manager)
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Portal-master
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and update it with your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Supabase Configuration
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_BUCKET_NAME=reports
```

**⚠️ IMPORTANT: Never commit your `.env` file to version control!**

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Project Structure

```
Portal-master/
├── manage.py
├── requirements.txt
├── .env.example
├── studetPortals/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── reports/                # Main application
    ├── models.py           # Database models
    ├── views.py            # View logic
    ├── forms.py            # Form definitions
    ├── urls.py             # URL routing
    ├── admin.py            # Admin interface
    ├── decorators.py       # Custom decorators
    ├── utils.py            # Utility functions
    ├── migrations/         # Database migrations
    └── templates/          # HTML templates
        └── reports/
```

## User Roles

### Student
- View enrolled courses
- Check grades and GPA
- Submit course reviews
- View academic reports

### Lecturer
- View assigned courses
- Manage course students
- Update student grades
- View course reviews

### Admin
- Full system access
- User management
- Course creation and management
- View all reports and reviews

## Security Notes

- **Never commit secrets**: Always use environment variables for sensitive data
- **Rotate compromised keys**: If you accidentally commit secrets, rotate them immediately
- **Use strong SECRET_KEY**: Generate a new Django secret key for production
- **Disable DEBUG in production**: Set `DEBUG=False` in production environments

## Supabase Setup

1. Create a Supabase account at https://supabase.com
2. Create a new project
3. Create a storage bucket named "reports"
4. Copy your project URL and anon key to `.env`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is for educational purposes.

## Support

For issues or questions, please open an issue in the repository.
