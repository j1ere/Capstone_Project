from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import *


class AuthViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]#allow anyone to register or login

    """account registration"""
    def register(self, request):
        serializer = UserSerializer(data=request.data)
     
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    """user login"""
    def login(self, request):
        username= request.data.get('username')
        password= request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message":"login successful", 'token':token.key}, status=status.HTTP_200_OK)
        return Response({"error":"incorrect username or password"}, status=status.HTTP_401_UNAUTHORIZED)
    

class UserTasksModelViewSet(viewsets.ModelViewSet):
    """models viewset for user tasks"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = UserTasks.objects.all()
    serializer_class = UserTasksSerializer

    def get_queryset(self):
        """limit tasks to the authenticated user"""
        return UserTasks.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """automatically assign the task to the logged in user"""
        serializer.save(user=self.request.user)

        
   