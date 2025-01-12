from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'usertasks', views.UserTasksModelViewSet, basename='usertasks')
router.register(r'groups', views.GroupModelViewSet, basename='groups')
router.register(r'join-requests', views.JoinRequestViewSet, basename='join-requests')
router.register(r'groups', views.GroupAdminViewSet, basename='group-admin')
router.register(r'groups/(?P<group_pk>\d+)/grouptasks', views.GroupTaskModelViewSet, basename='group-task')



urlpatterns=[
    path('auth/register/', views.AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('auth/login/', views.AuthViewSet.as_view({'post': 'login'}), name='login'),

    path('', include(router.urls)),
]