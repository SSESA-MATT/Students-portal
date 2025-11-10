from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from reports.models import Student, Course, Grade, CourseReview, Profile
from .serializers import (
    StudentSerializer, StudentDetailSerializer, CourseSerializer, 
    CourseDetailSerializer, GradeSerializer, CourseReviewSerializer,
    ProfileSerializer, EnrollmentSerializer
)
from .permissions import IsStudent, IsLecturer, IsAdmin, IsLecturerOrAdmin, IsOwnerOrReadOnly
from reports.utils import calculate_gpa, calculate_cgpa


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Student model
    
    list: Get all students (admin/lecturer only)
    retrieve: Get single student details
    me: Get current logged-in student details
    enroll: Enroll in a course
    unenroll: Unenroll from a course
    my_grades: Get grades for current student
    my_gpa: Get GPA/CGPA for current student
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'gpa']
    
    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'me':
            return StudentDetailSerializer
        return StudentSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'create', 'update', 'partial_update', 'destroy']:
            return [IsLecturerOrAdmin()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current logged-in student details"""
        try:
            student = Student.objects.get(user=request.user)
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(
                {"detail": "Student profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll student in a course"""
        student = self.get_object()
        
        # Only allow students to enroll themselves
        if hasattr(request.user, 'profile') and request.user.profile.role != 'student':
            if student.user != request.user:
                return Response(
                    {"detail": "You can only enroll yourself"},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            course = Course.objects.get(id=serializer.validated_data['course_id'])
            
            if student in course.students.all():
                return Response(
                    {"detail": "Already enrolled in this course"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            course.students.add(student)
            return Response(
                {"detail": f"Successfully enrolled in {course.name}"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def unenroll(self, request, pk=None):
        """Unenroll student from a course"""
        student = self.get_object()
        
        # Only allow students to unenroll themselves
        if hasattr(request.user, 'profile') and request.user.profile.role != 'student':
            if student.user != request.user:
                return Response(
                    {"detail": "You can only unenroll yourself"},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            course = Course.objects.get(id=serializer.validated_data['course_id'])
            
            if student not in course.students.all():
                return Response(
                    {"detail": "Not enrolled in this course"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            course.students.remove(student)
            return Response(
                {"detail": f"Successfully unenrolled from {course.name}"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def grades(self, request, pk=None):
        """Get all grades for a student"""
        student = self.get_object()
        grades = Grade.objects.filter(student=student)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def gpa(self, request, pk=None):
        """Get GPA and CGPA for a student"""
        student = self.get_object()
        return Response({
            'student_id': student.id,
            'student_name': student.name,
            'gpa': calculate_gpa(student),
            'cgpa': calculate_cgpa(student)
        })


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course model
    
    list: Get all courses
    retrieve: Get single course details
    students: Get all students enrolled in a course
    reviews: Get all reviews for a course
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['lecturer']
    search_fields = ['name', 'code', 'lecturer']
    ordering_fields = ['name', 'code']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLecturerOrAdmin()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students enrolled in a course"""
        course = self.get_object()
        
        # Get students from both M2M and grades
        students_from_m2m = list(course.students.all())
        students_from_grades = [grade.student for grade in Grade.objects.filter(course=course)]
        students = list({student.id: student for student in students_from_m2m + students_from_grades}.values())
        
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a course"""
        course = self.get_object()
        reviews = CourseReview.objects.filter(course=course)
        serializer = CourseReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class GradeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Grade model
    
    list: Get all grades (filtered by student/course)
    create: Create a new grade (lecturer/admin only)
    update: Update a grade (lecturer/admin only)
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'course', 'letter']
    ordering_fields = ['score', 'letter']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLecturerOrAdmin()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Filter grades based on user role"""
        queryset = Grade.objects.all()
        user = self.request.user
        
        if hasattr(user, 'profile'):
            if user.profile.role == 'student':
                # Students can only see their own grades
                try:
                    student = Student.objects.get(user=user)
                    queryset = queryset.filter(student=student)
                except Student.DoesNotExist:
                    queryset = queryset.none()
            elif user.profile.role == 'lecturer':
                # Lecturers can see grades for their courses
                lecturer_courses = Course.objects.filter(lecturer=user.profile.name)
                queryset = queryset.filter(course__in=lecturer_courses)
        
        return queryset


class CourseReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CourseReview model
    
    list: Get all reviews (filtered by course/student)
    create: Create a new review (student only)
    update: Update own review
    destroy: Delete own review
    """
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'student', 'rating']
    ordering_fields = ['rating', 'created_at']
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsStudent()]
        return [IsAuthenticated(), IsOwnerOrReadOnly()]
    
    def perform_create(self, serializer):
        """Auto-assign current student when creating review"""
        student = Student.objects.get(user=self.request.user)
        serializer.save(student=student)
    
    def get_queryset(self):
        """Filter reviews based on user role"""
        queryset = CourseReview.objects.all()
        user = self.request.user
        
        if hasattr(user, 'profile'):
            if user.profile.role == 'student':
                # Students can see all reviews but only edit their own
                pass
            elif user.profile.role == 'lecturer':
                # Lecturers can see reviews for their courses
                lecturer_courses = Course.objects.filter(lecturer=user.profile.name)
                queryset = queryset.filter(course__in=lecturer_courses)
        
        return queryset


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Profile model (read-only)
    
    list: Get all profiles (admin only)
    retrieve: Get single profile
    me: Get current user's profile
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']
    
    def get_permissions(self):
        if self.action == 'list':
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user.profile)
        return Response(serializer.data)
