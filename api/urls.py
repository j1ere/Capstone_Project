from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

router = DefaultRouter()

router.register(r'auth', views.AuthViewSet, basename='auth')

urlpatterns=[
    path('auth/register/', views.AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('auth/login/', views.AuthViewSet.as_view({'post': 'login'}), name='login'),

]+ router.urls