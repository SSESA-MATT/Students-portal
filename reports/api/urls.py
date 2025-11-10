from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    StudentViewSet, CourseViewSet, GradeViewSet, 
    CourseReviewViewSet, ProfileViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'reviews', CourseReviewViewSet, basename='review')
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
