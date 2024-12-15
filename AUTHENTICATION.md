# Authentication Setup for Task Management API

## Authentication Method: Session Authentication

In this project, we have implemented **Session Authentication**, which is the default authentication system in Django. This method relies on the user's session, which is maintained via cookies.

### Steps for Setting Up Session Authentication

1. **Install Django Rest Framework**
   - First, you need to install Django Rest Framework (DRF) if it's not already installed in your project:
     ```bash
     pip install djangorestframework
     ```

2. **Update `INSTALLED_APPS`**
   - Open the `settings.py` file and add `rest_framework` to the `INSTALLED_APPS` list:
     ```python
     INSTALLED_APPS = [
         # other apps
         'rest_framework',
         'api',  # your app
     ]
     ```

3. **Configure Session Authentication**
   - In `settings.py`, update the `REST_FRAMEWORK` configuration to use session authentication:
     ```python
     REST_FRAMEWORK = {
         'DEFAULT_AUTHENTICATION_CLASSES': [
             'rest_framework.authentication.SessionAuthentication',  # Session Authentication
         ],
         'DEFAULT_PERMISSION_CLASSES': [
             'rest_framework.permissions.IsAuthenticated',  # Ensure user is authenticated
         ]
     }
     ```

4. **Create API View with Authentication**
   - In your `views.py` file, you can create views that require authentication. Here's an example view for listing tasks:
     ```python
     from rest_framework.views import APIView
     from rest_framework.response import Response
     from rest_framework.permissions import IsAuthenticated
     from rest_framework import status
     from .models import Task

     class TaskListView(APIView):
         permission_classes = [IsAuthenticated]

         def get(self, request):
             tasks = Task.objects.filter(user=request.user)
             # Serialize the tasks here (e.g., using Django Rest Framework serializers)
             return Response({"tasks": tasks}, status=status.HTTP_200_OK)
     ```

5. **Add URL for the Task List API**
   - In your `urls.py` file, add the URL path for the task list view:
     ```python
     from django.urls import path
     from .views import TaskListView

     urlpatterns = [
         path('tasks/', TaskListView.as_view(), name='task-list'),
     ]
     ```

### Testing Session Authentication

1. **Log in via Django's Admin Interface**
   - Use Django's built-in admin interface (`/admin`) to log in with a user account.
   - Once logged in, the session cookie will be stored in your browser automatically.

2. **Test the API Endpoint**
   - Open your browser or Postman and test the `GET /tasks/` endpoint.
   - The request will be authenticated via the session cookie, and only the tasks of the authenticated user will be returned.

3. **Error Handling**
   - If the user is not authenticated, you will receive a `401 Unauthorized` response.
   - Example error response:
     ```json
     {
         "detail": "Authentication credentials were not provided."
     }
     ```

4. **Testing with Postman**
   - To test the API in Postman, make sure you are logged in via Django's admin interface first.
   - Send a `GET` request to `http://127.0.0.1:8000/tasks/` and ensure that the session cookie is included in the request headers.

### Example Request and Response

**Request (GET /tasks/):**
- **Headers:** The request must include the session cookie, which is sent automatically by the browser after logging in via the Django admin interface.
  
**Response:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Task 1",
      "description": "Description of task 1",
      "due_date": "2024-12-31",
      "status": "pending",
      "created_at": "2024-12-15T00:00:00Z",
      "updated_at": "2024-12-15T00:00:00Z"
    },
    {
      "id": 2,
      "title": "Task 2",
      "description": "Description of task 2",
      "due_date": "2024-12-20",
      "status": "completed",
      "created_at": "2024-12-10T00:00:00Z",
      "updated_at": "2024-12-10T00:00:00Z"
    }
  ]
}
