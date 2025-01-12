# API Endpoints Documentation

## Authentication Endpoints
### all urls start with a `/api/`

### `POST /auth/register/`
- **Description**: Register a new user.
- **Request Body**:
  ```json
  {
      "username": "string",
      "email": "email",
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
  - insert the token in your header for authentication

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
      "task_title": "Prepare Report",
      "task_category": "work",
      "task_priority": "medium",
      "task_description": "Complete the quarterly report.",
      "deadline": "2025-02-20T10:00:00Z"
  }
  ```
- **Response**:
  ```json
  {
        "task_title": "Prepare Report",
        "task_category": "Work",
        "task_priority": "medium",
        "task_description": "Complete the quarterly report.",
        "deadline": "2025-02-20T10:00:00Z",
        "is_complete": false,
        "completed_at": null
  }

  ```

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

### `GET api/usertasks/?task_category=personal&ordering=-deadline`

### `GET api/usertasks/?is_complete=true`

### `GET api/usertasks/?is_complete=false`

### `GET api/usertasks/?itask_priority=low`
---

## Group Endpoints
- **Create Two Accounts**:
    - Register/Login User A (the user who will send the join request).
    - Register/Login User B (the user who will act as the group admin).
    - insert the token in your header for authentication

- **Step 2: Create a Group with User B (Admin)**:


### `GET /groups/`
- **Description**: Retrieve a list of groups.
- **Response**:
  - `200 OK`: List of groups.

### `POST /groups/`
- **Description**: Create a new group.
- **Request Body**:
  ```json
  {
     "company_name": "JeremyTech",
     "group_name": "Co-founders",
     "members": [3,] //members in a list
  }

  ```
- **Response**:
  - `200 OK`: List of the group.

### `POST /groups/{id}/add-admin/`
- **Description**: Add a user as an admin to a group.
- **Request Body**:
  ```json
  {
      "user_id": "integer"
  }
  ```
- **Response**:
  - `201 Created`: User added as admin successfully.
  - `400 Bad Request`: User ID not provided.
  - `404 Not Found`: User does not exist.

---

## Join Request Endpoints

### `POST /join-requests/`
- **Description**: Send a join request to a group.
- **Request Body**:
  ```json
  {
     "user": "<user id>",
     "group": "<group id>"
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

### `POST /groups/{id}/approve-join-requests/`
- **Request Body**:
  ```json
  {
      "user_id": "integer"
  }
  ```

### `POST /groups/{id}/deny-join-requests/`
- **Request Body**:
  ```json
  {
      "user_id": "integer"
  }
  ```

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
     "task_title": "Fix Bugs",
     "assigned_to": 3,  // ID of the member
     "task_priority": "high",
     "task_description": "Resolve critical bugs in the system",
     "deadline": "2025-01-15T18:00:00Z"
   }

  ```
- **Response**:
  - `201 Created`: Task created successfully.

### `DELETE api/groups/1/grouptasks/5/`

### `PUT api/groups/1/grouptasks/5/`

### `GET /groups/{id}/my-tasks/`
- **Description**: Retrieve tasks assigned to the authenticated user within a group.
- **Response**:
  - `200 OK`: List of tasks assigned to the user.

