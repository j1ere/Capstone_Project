# API Endpoints Documentation

## Authentication Endpoints

### `POST /auth/register/`
- **Description**: Register a new user.
- **Request Body**:
  ```json
  {
      "username": "string",
      "password": "string"
  }
  ```
- **Response**:
  - `201 Created`: User created successfully.
  - `400 Bad Request`: Validation errors.

### `POST /auth/login/`
- **Description**: Authenticate a user and return a token.
- **Request Body**:
  ```json
  {
      "username": "string",
      "password": "string"
  }
  ```
- **Response**:
  - `200 OK`: Login successful with token.
  - `401 Unauthorized`: Incorrect username or password.

---

## User Tasks Endpoints

### `GET /usertasks/`
- **Description**: Retrieve a list of tasks for the authenticated user.
- **Query Parameters**:
  - `task_category` (optional): Filter by task category.
  - `task_priority` (optional): Filter by task priority.
  - `is_complete` (optional): Filter by completion status.
  - `deadline` (optional): Filter by deadline.
- **Response**:
  - `200 OK`: List of tasks.

### `POST /usertasks/`
- **Description**: Create a new task for the authenticated user.
- **Request Body**:
  ```json
  {
      "title": "string",
      "description": "string",
      "task_category": "string",
      "task_priority": "string",
      "deadline": "YYYY-MM-DDTHH:MM:SSZ"
  }
  ```
- **Response**:
  - `201 Created`: Task created successfully.

### `PATCH /usertasks/{id}/mark-complete/`
- **Description**: Mark a task as complete.
- **Response**:
  - `200 OK`: Task marked as complete.
  - `400 Bad Request`: Task is already marked as complete.

### `PATCH /usertasks/{id}/mark-incomplete/`
- **Description**: Mark a task as incomplete.
- **Response**:
  - `200 OK`: Task marked as incomplete.
  - `400 Bad Request`: Task is already incomplete.

---

## Group Endpoints

### `GET /groups/`
- **Description**: Retrieve a list of groups.
- **Response**:
  - `200 OK`: List of groups.

### `POST /groups/`
- **Description**: Create a new group.
- **Request Body**:
  ```json
  {
      "name": "string",
      "description": "string"
  }
  ```
- **Response**:
  - `201 Created`: Group created successfully.

### `POST /groups/{id}/add-admin/`
- **Description**: Add a user as an admin to a group.
- **Request Body**:
  ```json
  {
      "user_id": "integer"
  }
  ```
- **Response**:
  - `201 Created`: User added as admin.
  - `400 Bad Request`: User ID not provided.
  - `404 Not Found`: User does not exist.

---

## Join Request Endpoints

### `POST /join-requests/`
- **Description**: Send a join request to a group.
- **Request Body**:
  ```json
  {
      "group": "integer"
  }
  ```
- **Response**:
  - `201 Created`: Join request sent successfully.
  - `400 Bad Request`: User is already a member or join request already exists.
  - `404 Not Found`: Group not found.

### `POST /groups/{id}/approve-join-request/`
- **Description**: Approve a join request for a group.
- **Request Body**:
  ```json
  {
      "user_id": "integer"
  }
  ```
- **Response**:
  - `200 OK`: Join request approved.
  - `400 Bad Request`: User ID not provided.
  - `403 Forbidden`: Only admins can approve join requests.
  - `404 Not Found`: Group or join request not found.

### `POST /groups/{id}/deny-join-request/`
- **Description**: Deny a join request for a group.
- **Request Body**:
  ```json
  {
      "user_id": "integer"
  }
  ```
- **Response**:
  - `200 OK`: Join request denied.
  - `400 Bad Request`: User ID not provided.
  - `403 Forbidden`: Only admins can deny join requests.
  - `404 Not Found`: Group or join request not found.

### `GET /groups/{id}/pending-join-requests/`
- **Description**: List all pending join requests for a group.
- **Response**:
  - `200 OK`: List of pending join requests.

---

## Group Task Endpoints

### `GET /groups/{group_pk}/grouptasks/`
- **Description**: Retrieve tasks for a specific group.
- **Response**:
  - `200 OK`: List of group tasks.

### `POST /groups/{group_pk}/grouptasks/`
- **Description**: Create a new task for a group.
- **Request Body**:
  ```json
  {
      "title": "string",
      "description": "string",
      "assigned_to": "integer",
      "due_date": "YYYY-MM-DDTHH:MM:SSZ"
  }
  ```
- **Response**:
  - `201 Created`: Task created successfully.

### `GET /groups/{id}/my-tasks/`
- **Description**: Retrieve tasks assigned to the authenticated user within a group.
- **Response**:
  - `200 OK`: List of tasks assigned to the user.

