from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserQueryViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'user_queries', UserQueryViewSet, basename='user_query')

urlpatterns = [
    path('', include(router.urls)),
]