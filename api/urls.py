from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'usertasks', views.UserTasksModelViewSet, basename='usertasks')

urlpatterns=[
    path('auth/register/', views.AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('auth/login/', views.AuthViewSet.as_view({'post': 'login'}), name='login'),

    path('', include(router.urls)),
]