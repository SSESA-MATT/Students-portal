from rest_framework import serializers
from django.contrib.auth.models import User
from reports.models import Student, Course, Grade, CourseReview, Profile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'name', 'courses']
        read_only_fields = ['id']


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    user = UserSerializer(read_only=True)
    gpa = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'name', 'email', 'gpa']
        read_only_fields = ['id', 'gpa']


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model"""
    student_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'credit_units', 'lecturer', 'student_count']
        read_only_fields = ['id']
    
    def get_student_count(self, obj):
        return obj.students.count()


class CourseDetailSerializer(CourseSerializer):
    """Detailed serializer for Course with students"""
    students = StudentSerializer(many=True, read_only=True)
    
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['students']


class GradeSerializer(serializers.ModelSerializer):
    """Serializer for Grade model"""
    student_name = serializers.CharField(source='student.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    letter = serializers.CharField(read_only=True)
    grade_point = serializers.FloatField(read_only=True)
    np_status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Grade
        fields = ['id', 'student', 'student_name', 'course', 'course_name', 
                  'course_code', 'score', 'letter', 'grade_point', 'np_status']
        read_only_fields = ['id', 'letter', 'grade_point']


class CourseReviewSerializer(serializers.ModelSerializer):
    """Serializer for CourseReview model"""
    student_name = serializers.CharField(source='student.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = CourseReview
        fields = ['id', 'course', 'course_name', 'student', 'student_name', 
                  'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_rating(self, value):
        """Validate rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value


class StudentDetailSerializer(StudentSerializer):
    """Detailed serializer for Student with courses and grades"""
    enrolled_courses = CourseSerializer(source='courses', many=True, read_only=True)
    grades = GradeSerializer(many=True, read_only=True, source='grade_set')
    gpa = serializers.SerializerMethodField()
    cgpa = serializers.SerializerMethodField()
    semester_remark = serializers.SerializerMethodField()
    
    class Meta(StudentSerializer.Meta):
        fields = StudentSerializer.Meta.fields + ['enrolled_courses', 'grades', 'cgpa', 'semester_remark']
    
    def get_gpa(self, obj):
        """Calculate GPA"""
        from reports.utils import calculate_gpa
        return calculate_gpa(obj)
    
    def get_cgpa(self, obj):
        """Calculate CGPA"""
        from reports.utils import calculate_cgpa
        return calculate_cgpa(obj)
    
    def get_semester_remark(self, obj):
        """Get semester remark based on grades"""
        grades = Grade.objects.filter(student=obj)
        if not grades.exists():
            return "No grades yet"
        if all(grade.np_status == "NP" for grade in grades):
            return "Normal Progress"
        return "Attention Needed"


class EnrollmentSerializer(serializers.Serializer):
    """Serializer for course enrollment"""
    course_id = serializers.IntegerField()
    
    def validate_course_id(self, value):
        """Validate course exists"""
        try:
            Course.objects.get(id=value)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course does not exist")
        return value
