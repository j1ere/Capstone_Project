from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated


class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['user'] = request.user.id  # Assign task to the authenticated user

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the task to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TaskListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         tasks = Task.objects.filter(user=request.user)  # Get tasks of the authenticated user
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response({"tasks": tasks}, status=status.HTTP_200_OK)