"""
Module 6 Project — AI Dashboard  (STARTER)
API Client
============
Centralised functions for all backend communication.

All API calls should go through these functions so that:
    • The Authorization header is added in one place
    • Error handling is consistent
    • The rest of the app stays clean

Functions to implement:
    login(username, password)   → (token: str | None, error: str | None)
    get_tasks(token)            → (tasks: list | None, error: str | None)
    create_task(token, title)   → (task: dict | None, error: str | None)
    complete_task(token, task_id) → (task: dict | None, error: str | None)
"""

import requests

API_BASE = "http://localhost:8000"


def login(username: str, password: str):
    """
    POST /auth/token with username and password.
    Returns (access_token, None) on success or (None, error_message) on failure.

    TODO: Implement this function.
    Steps:
      1. requests.post(API_BASE + "/auth/token", data={...})
         NOTE: If you're using your own Module 5 API (Option A, recommended),
         this endpoint expects form-encoded data (OAuth2PasswordRequestForm),
         not JSON — use `data=`, not `json=`, or you'll get a 422 error.
         Using the Lesson 11 demo backend instead (Option B)? That one expects
         a JSON body, so use `json=` there.
      2. Check response.ok — if not, return (None, error message)
      3. Parse response.json() — return the access_token
      4. Catch requests.ConnectionError
    """
    # TODO: implement
    try:
        response = requests.post(
            API_BASE + "/auth/token",
            data={
                "username": username,
                "password": password
            },
            timeout=10
        )

        if response.status_code == 401:
            return None, "Invalid username or password"

        response.raise_for_status()

        token = response.json()["access_token"]
        return token, None

    except requests.ConnectionError:
        return None, "Cannot connect to the FastAPI backend"

    except requests.RequestException as error:
        return None, str(error)


def get_tasks(token: str):
    """
    GET /tasks with Bearer token.
    Returns (list_of_tasks, None) or (None, error_message).

    TODO: Implement this function.
    Include the header: {"Authorization": f"Bearer {token}"}
    """
    try:
        response = requests.get(
            API_BASE + "/tasks/",
            headers={
                "Authorization": f"Bearer {token}"
            },
            timeout=10
        )

        if response.status_code == 401:
            return None, "Session expired or invalid token"

        response.raise_for_status()

        tasks = response.json()
        return tasks, None

    except requests.ConnectionError:
        return None, "Cannot connect to the FastAPI backend"

    except requests.RequestException as error:
        return None, str(error)


def create_task(token: str, title: str):
    """
    POST /tasks with Bearer token and JSON body {"title": title}.
    Returns (new_task_dict, None) or (None, error_message).

    TODO: Implement this function.
    """
    # TODO: implement
    try:
        response = requests.post(
            API_BASE + "/tasks/",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "title": title,
                "completed": False,
                "priority": "medium"
            },
            timeout=10
        )

        if response.status_code == 401:
            return None, "Session expired or invalid token"

        response.raise_for_status()

        new_task = response.json()
        return new_task, None

    except requests.ConnectionError:
        return None, "Cannot connect to the FastAPI backend"

    except requests.RequestException as error:
        return None, str(error)


def complete_task(token: str, task_id: int):
    """
    PATCH /tasks/{task_id} with Bearer token and JSON body {"completed": True}.
    Returns (updated_task_dict, None) or (None, error_message).

    TODO: Implement this function.
    NOTE: Your own Module 5 API (Option A, recommended) almost certainly has no
    dedicated "/complete" route — it uses this generic PATCH endpoint for partial
    updates instead. The Lesson 11 demo backend (Option B) is the one with a
    dedicated PATCH /tasks/{task_id}/complete route; adjust the URL below if
    you're using that backend instead.
    """
    # TODO: implement

    try:
        response = requests.patch(
            API_BASE + f"/tasks/{task_id}",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={"completed": True},
            timeout=10
        )

        if response.status_code == 401:
            return None, "Session expired or invalid token"

        response.raise_for_status()

        updated_task = response.json()
        return updated_task, None

    except requests.ConnectionError:
        return None, "Cannot connect to the FastAPI backend"

    except requests.RequestException as error:
        return None, str(error)
