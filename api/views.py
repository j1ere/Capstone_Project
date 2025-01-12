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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied

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

    #add filtering backend and filter fields
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task_category', 'task_priority'] 

    def get_queryset(self):
        """limit tasks to the authenticated user"""
        return UserTasks.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """automatically assign the task to the logged in user"""
        serializer.save(user=self.request.user)


class GroupModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Groups.objects.all()
    serializer_class = GroupSerializer

    @action(detail=True, methods=['POST'], url_path='add-admin')
    def add_admin(self, request, pk=None):
        """custom action to add an admin to the group"""
        group = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'User ID is required'}, status=400)
        
        try:
            user = User.objects.get(id=user_id)
            group.add_admin(user)
            return Response({'message': f"{user.username} made group admin successfully"}, status=status.HTTP_201_CREATED)
        except user.DoesNotExist:
            return Response({'error': 'user does not exist'}, status=404)
            

class JoinRequestViewSet(viewsets.ModelViewSet):
    queryset = JoinRequest.objects.all()
    serializer = JoinRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        group_id = request.data.get('group')
        
        if not group_id:
            return Response({"error": "Group ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            group = Groups.objects.get(id=group_id)
        except Groups.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the user is already a member or has a pending join request
        if Membership.objects.filter(user=user, group=group).exists():
            return Response({"error": "User is already a member of the group"}, status=status.HTTP_400_BAD_REQUEST)
        
        if JoinRequest.objects.filter(user=user, group=group).exists():
            return Response({"error": "Join request already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the join request
        join_request = JoinRequest.objects.create(user=user, group=group)
        
        return Response({"message": "Join request sent successfully"}, status=status.HTTP_201_CREATED)


class GroupAdminViewSet(viewsets.ViewSet):
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated]

     @action(detail=True, methods=['post'], url_path='approve-join-request')
     def approve_join_request(self, request, pk=None):
         """approve a join request for a group by group admin"""
         try:
             group = Groups.objects.get(id=pk)
         except Groups.DoesNotExist:
             return Response({'error': 'group not found'}, status=status.HTTP_404_NOT_FOUND)
         
         if not group.is_admin(request.user):
             return Response({'error': 'only admins can approve join requests'}, status=status.HTTP_403_FORBIDDEN)
         
         user_id = request.data.get('user_id')
         if not user_id:
             return Response({'error': 'user id is required'}, status=status.HTTP_400_BAD_REQUEST)
         
         join_request = JoinRequest.objects.filter(user_id=user_id, group=group, is_approved=False).first()

         if not join_request:
             return Response({'error': 'join request not found or already approved'})

         #approve the join request
         Membership.objects.create(user=join_request.user, group=group, role='member')
         join_request.is_approved=True
         join_request.save()

         return Response({'message': 'join request approved'}, status=status.HTTP_200_OK)

     @action(detail=True, methods=['post'], url_path='deny-join-request')
     def deny_join_request(self, request, pk=None):
         """deny a join request for the group by group admin"""
         try:
            group = Groups.objects.get(id=pk)
         except Groups.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

         if not group.is_admin(request.user):
            return Response({"error": "Only admins can deny join requests"}, status=status.HTTP_403_FORBIDDEN)

         user_id = request.data.get('user_id')
         if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

         join_request = JoinRequest.objects.filter(user_id=user_id, group=group, is_approved=False).first()

         if not join_request:
            return Response({"error": "Join request not found or already approved"}, status=status.HTTP_404_NOT_FOUND)

         # Deny the join request
         join_request.delete()

         return Response({"message": "Join request denied"}, status=status.HTTP_200_OK)
                   
     @action(detail=True, methods=['GET'], url_path='pending-join-requests')
     def pending_join_requests(self, request, pk=None):
        """List all pending join requests for a group"""
        try:
            group = Groups.objects.get(pk=pk)
        except Groups.DoesNotExist:
            raise NotFound("Group not found.")
    
        pending_requests = JoinRequest.objects.filter(group=group, is_approved=False)
        serializer = JoinRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=200)
     
    
     @action(detail=True, methods=['GET'], url_path='my-tasks')
     def my_tasks(self, request, pk=None):
        """Allow a user to view tasks assigned to them"""
        user = request.user
        tasks = GroupTasks.objects.filter(assigned_to=user)
        serializer = GroupTaskSerializer(tasks, many=True)
        return Response(serializer.data, status=200)


from .permissions import IsGroupAdminOrReadOnly

class GroupTaskModelViewSet(viewsets.ModelViewSet):
    queryset = GroupTasks.objects.all()
    serializer_class = GroupTaskSerializer
    permission_classes = [IsAuthenticated, IsGroupAdminOrReadOnly]

    def get_queryset(self):
        """
        Filter tasks based on the group ID from the URL.
        """
        group_id = self.kwargs['group_pk']
        return GroupTasks.objects.filter(group_id=group_id)

    def perform_create(self, serializer):
        """
        Assign the task to the current authenticated user when creating.
        """
        serializer.save(assigned_to=self.request.user)

# class GroupAdminViewSet(viewsets.ModelViewSet):
#     queryset = Groups.objects.all()
#     serializer_class = GroupSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]


#     @action(detail=True, methods=['POST'], url_path='create-task')
#     def create_task(self, request, pk=None):
#         """Allow an admin to create a task for a group"""
#         group = self.get_object()
#         user = request.user

#         # Check if the user is an admin of the group
#         if not group.is_admin(user):
#             raise PermissionDenied("You must be an admin to create tasks.")

#         serializer = GroupTaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

#     @action(detail=True, methods=['GET'], url_path='my-tasks')
#     def my_tasks(self, request, pk=None):
#         """Allow a user to view tasks assigned to them"""
#         user = request.user
#         tasks = GroupTasks.objects.filter(assigned_to=user)
#         serializer = GroupTaskSerializer(tasks, many=True)
#         return Response(serializer.data, status=200)