from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ProjectViewSet
from .auth_views import UserRegistrationView, CustomAuthToken

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
]