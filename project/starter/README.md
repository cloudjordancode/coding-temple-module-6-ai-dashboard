# AI Dashboard — Coding Temple Module 6 Final Project

## Project Overview

AI Dashboard is a full-stack task management application built with Streamlit and FastAPI. It combines secure user authentication, task management, dashboard analytics, and a simulated AI chat interface.

The application integrates the Module 5 AI-Ready Task Manager API as an independent backend.

## Features

- JWT-based user authentication and logout
- User-specific task management
- Create tasks and mark tasks as completed
- Dashboard metrics for total, completed, and pending tasks
- Task overview table and status chart
- AI chat with conversation history and simulated streaming responses
- Mock data mode for offline interface testing
- SQLite database for persistent task storage

## Technology Stack

- Python
- Streamlit — frontend
- FastAPI — backend
- SQLAlchemy — database ORM
- SQLite — database
- Pydantic — data validation
- JWT — authentication
- Requests — frontend/backend communication

## Project Structure

```text
project/starter/
├── app.py
├── api_client.py
├── mock_data.py
├── requirements.txt
├── README.md
└── backend/
    ├── app/
    │   ├── models/
    │   ├── routers/
    │   ├── schemas/
    │   ├── utils/
    │   ├── auth.py
    │   ├── database.py
    │   └── main.py
    ├── .env.example
    └── requirements.txt
```

## Installation

**Python requirement:** Python 3.10 or newer is recommended.

From the Module 6 project directory:

1. Create and activate a Python virtual environment.
2. Install frontend dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Install backend dependencies:

```bash
python -m pip install -r backend/requirements.txt
```

4. Create `backend/.env` using `backend/.env.example` as a template. Generate a secure JWT secret:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Set `SECRET_KEY` in the local `.env` file to the generated value. Never commit the secret to Git.

## Running the Application

### Start FastAPI

From `project/starter`:

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Swagger documentation:

http://127.0.0.1:8000/docs

### Start Streamlit

In a second terminal, return to `project/starter`:

```bash
python -m streamlit run app.py
```

Open:

http://localhost:8501

## Usage

1. Register a user using the FastAPI Swagger interface at `/auth/register`.
2. Log in through Streamlit with the registered credentials.
3. Create and complete tasks using the Tasks tab.
4. View task metrics and charts on the Dashboard tab.
5. Use the AI Chat tab for simulated assistant conversations.
6. Log out using the sidebar.

## Mock Mode

The application supports mock data mode for testing the interface without relying on the backend. Select **Use Mock Data** on the login screen to test sample tasks, dashboard metrics, and task interactions.

Mock data is separate from the persistent SQLite backend.

## Testing

The following functionality was manually verified:

- User registration and JWT login
- Task creation and retrieval through FastAPI
- Streamlit task creation and completion
- Dashboard metrics and chart updates
- Task persistence after refresh, logout, and login
- Mock mode functionality
- AI chat responses, conversation history, and streaming
- Logout and session management

## Security

- JWT authentication protects API endpoints.
- Task queries are restricted to the authenticated user.
- Passwords are hashed before storage.
- Local environment files and databases are excluded from version control.
- Development secrets must be replaced with secure values.

## Project Notes

This project demonstrates integration between a Python web frontend, a REST API, authentication, database persistence, and an AI-style user interface.

The AI chat currently uses simulated responses rather than a live language model API.

## Author

Coding Temple — AI Software Engineering, Module 6 Final Project
