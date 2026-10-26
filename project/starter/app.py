"""
Module 6 Project — AI Dashboard  (STARTER)
==========================================
Run with:
    # Start the backend (when ready):
    uvicorn backend:app --reload --port 8000

    # Start the Streamlit app:
    streamlit run app.py

Your goal: build a full Streamlit dashboard with authentication,
task management, data visualisation, and an AI chat feature.

Required sections (each marked with TODO):
    1. Authentication — login form, JWT in session state, logout
    2. Dashboard view — metrics, task list, chart
    3. Data interaction — add task form, complete task buttons
    4. AI chat feature — chat history, mock responses, streaming
    5. Layout — sidebar, tabs, metrics, error messages

Import the API functions from api_client.py (not requests directly).
Use mock_data.py to test the UI while the backend is being built.
"""

import streamlit as st
from mock_data import MOCK_TASKS, MOCK_STATS, MOCK_USER, MOCK_TOKEN
import api_client
import time

def stream_response(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.04)

# ── Step 1: Page configuration ─────────────────────────────────────────────
st.set_page_config(layout="wide", page_title="AI Dashboard", page_icon="🤖")

# ── Step 2: Session state initialisation ───────────────────────────────────
# TODO: Initialise all session state keys you will need:
#   "token"    → None
#   "username" → None
#   "messages" → []    (chat history)
#   "use_mock" → False (toggle to use mock data instead of the real API)

if "token" not in st.session_state:
    st.session_state["token"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "use_mock" not in st.session_state:
    st.session_state["use_mock"] = False

if "tasks" not in st.session_state:
    st.session_state["tasks"] = [task.copy() for task in MOCK_TASKS]

# ════════════════════════════════════════════════════════════════════════════
# SECTION A — AUTHENTICATION
# ════════════════════════════════════════════════════════════════════════════
# TODO: Auth gate — if no token, show login form and st.stop()
#
# Login form should:
#   - Have username + password fields
#   - Have a "Use Mock Data" checkbox (sets token = MOCK_TOKEN, username = MOCK_USER)
#   - On real login: call api_client.login(username, password)
#   - Store token + username in session state on success
#   - Show st.error on failure
#   - Call st.rerun() after successful login


if st.session_state["token"] is None:
    st.title("🔐 AI Dashboard Login")
    st.write("Sign in to access your dashboard.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        use_mock = st.checkbox(
            "Use Mock Data",
            value=st.session_state["use_mock"]
        )

        submitted = st.form_submit_button("Login")

    if submitted:
        st.session_state["use_mock"] = use_mock

        if use_mock:
            st.session_state["token"] = MOCK_TOKEN
            st.session_state["username"] = MOCK_USER
            st.rerun()

        else:
            token, error = api_client.login(username, password)

            if error:
                st.error(error)
            else:
                st.session_state["token"] = token
                st.session_state["username"] = username
                st.rerun()
    st.stop()


# ════════════════════════════════════════════════════════════════════════════
# SECTION B — SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
# TODO: with st.sidebar:
#   - App title and divider
#   - "Logged in as [username]"
#   - Logout button (clear token/username, st.rerun())
#   - AI Chat settings (API key input, system prompt)
#   - Divider and caption

with st.sidebar:
    st.title("🤖 AI Dashboard")
    st.divider()

    st.write(f"Logged in as: {st.session_state['username']}")

    if st.button("Logout"):
        st.session_state["token"] = None
        st.session_state["username"] = None
        st.rerun()

    st.divider()

    st.subheader("AI Chat Settings")

    st.caption("AI responses are currently simulated.")

    st.divider()

    st.caption("Coding Temple | Module 6 Project")

# ════════════════════════════════════════════════════════════════════════════
# SECTION C — MAIN CONTENT (tabs)
# ════════════════════════════════════════════════════════════════════════════
# TODO: Create 3 tabs: "📊 Dashboard", "✅ Tasks", "🤖 AI Chat"

tab_dash, tab_tasks, tab_chat = st.tabs(["📊 Dashboard", "✅ Tasks", "🤖 AI Chat"])

# ── TAB 1: Dashboard ──────────────────────────────────────────────────────
# TODO: with tab_dash:
#   - Load tasks (or use MOCK_TASKS if in mock mode)
#   - Show 3 st.metric() in 3 columns: total, done, pending
#   - Show st.dataframe() with task data
#   - Show a bar chart of done vs pending

with tab_dash:
    st.header("Task Dashboard")

    if st.session_state["use_mock"]:
        tasks = st.session_state["tasks"]
    else:
        with st.spinner("Loading tasks..."):
            api_tasks, error = api_client.get_tasks(
                st.session_state["token"]
            )

        if error:
            st.error(error)
            tasks = []
        else:
            tasks = [
                {
                    "id": task["id"],
                    "title": task["title"],
                    "done": task["completed"],
                    "created_at": "N/A"
                }
                for task in api_tasks
            ]

    stats = {
        "total_tasks": len(tasks),
        "done_tasks": sum(1 for task in tasks if task["done"]),
        "pending_tasks": sum(1 for task in tasks if not task["done"])
    }

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Tasks", stats["total_tasks"])

    with col2:
        st.metric("Completed", stats["done_tasks"])

    with col3:
        st.metric("Pending", stats["pending_tasks"])


    st.subheader("Task Overview")

    st.dataframe(
        tasks,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Task Status")

    chart_data = {
        "Completed": stats["done_tasks"],
        "Pending": stats["pending_tasks"]
    }

    st.bar_chart(chart_data)


# ── TAB 2: Tasks ──────────────────────────────────────────────────────────
# TODO: with tab_tasks:
#   - Add task form (POST to API or append to mock data)
#   - Task list with Complete buttons (PATCH to API or update mock)
#   - Error handling for API failures
with tab_tasks:
    st.header("Task Management")

    with st.form("add_task_form", clear_on_submit=True):
        new_title = st.text_input("Task Title")
        submitted = st.form_submit_button("Add Task")

    st.subheader("Your Tasks")

    if st.session_state["use_mock"]:
        task_list = st.session_state["tasks"]
    else:
        api_tasks, error = api_client.get_tasks(
            st.session_state["token"]
        )

        if error:
            st.error(error)
            task_list = []
        else:
            task_list = [
                {
                    "id": task["id"],
                    "title": task["title"],
                    "done": task["completed"]
                }
                for task in api_tasks
            ]

    for task in task_list:
        col1, col2 = st.columns([4, 1])

        with col1:
            if task["done"]:
                st.write(f"✅ {task['title']}")
            else:
                st.write(f"⏳ {task['title']}")

        with col2:
            if not task["done"]:
                if st.button("Complete", key=f"complete_{task['id']}"):

                    if st.session_state["use_mock"]:
                        task["done"] = True
                        st.rerun()

                    else:
                        updated_task, error = api_client.complete_task(
                            st.session_state["token"],
                            task["id"]
                        )

                        if error:
                            st.error(error)
                        else:
                            st.rerun()

        if submitted:
            if not new_title.strip():
                st.error("Please enter a task title.")

            elif st.session_state["use_mock"]:
                new_task = {
                    "id": max(
                        (task["id"] for task in st.session_state["tasks"]),
                        default=0
                    ) + 1,
                    "title": new_title.strip(),
                    "done": False,
                    "created_at": str(__import__("datetime").date.today())
                }

                st.session_state["tasks"].append(new_task)
                st.success("Mock task added!")
                st.rerun()

            else:
                new_task, error = api_client.create_task(
                    st.session_state["token"],
                    new_title.strip()
                )

                if error:
                    st.error(error)
                else:
                    st.success("Task saved to FastAPI!")
                    st.rerun()


# ── TAB 3: AI Chat ────────────────────────────────────────────────────────
# TODO: with tab_chat:
#   - Render chat history (st.chat_message for each message)
#   - st.chat_input for user messages
#   - Mock response generator or real OpenAI call
#   - st.write_stream for streaming display
#   - Append both user and assistant messages to session state

with tab_chat:
    st.header("AI Assistant")

    if st.button("🗑️ Clear Chat"):
        st.session_state["messages"] = []
        st.rerun()

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Ask your AI assistant something...")

    if prompt:
        st.session_state["messages"].append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = (
                        f"You asked: {prompt}\n\n"
                        "This is a mock AI response from your dashboard. "
                        "A real AI model can be connected later."
                    )

                assistant_response = st.write_stream(
                    stream_response(response)
                )

            st.session_state["messages"].append({
                "role": "assistant",
                "content": assistant_response
            })