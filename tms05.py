import streamlit as st
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# User credentials
admin_username = "admin"
admin_password = "admin123"

team_head_username = "teamhead"
team_head_password = "head123"

team_member_username = "teammember"
team_member_password = "member123"

# User roles
ROLES = ["Admin", "Team Head", "Team Member"]

# User storage
@st.cache_resource("users")
def get_users():
    return {
        admin_username: {"password": admin_password, "role": "Admin"},
        team_head_username: {"password": team_head_password, "role": "Team Head"},
        team_member_username: {"password": team_member_password, "role": "Team Member"},
    }

users = get_users()

# Project storage
@st.cache_resource("projects")
def get_projects():
    return []

projects = get_projects()

# Task storage
@st.cache_resource("tasks")
def get_tasks():
    return []

tasks = get_tasks()

# Function to check user credentials
@st.cache(allow_output_mutation=True)
def check_credentials(username, password, role):
    users = get_users()
    user = users.get(username)
    if user and user["password"] == password and user["role"] == role:
        return True
    return False

# Function to add a new user
@st.cache(allow_output_mutation=True)
def add_user(username, password, role):
    users = get_users()
    users[username] = {"password": password, "role": role}

# Function to delete a user
@st.cache(allow_output_mutation=True)
def delete_user(username):
    users = get_users()
    if username in users:
        del users[username]

# Function to update a user's role
@st.cache(allow_output_mutation=True)
def update_user_role(username, new_role):
    users = get_users()
    if username in users:
        users[username]["role"] = new_role

# Function to create a new project
@st.cache(allow_output_mutation=True)
def create_project(name):
    projects = get_projects()
    project = {"name": name, "tasks": [], "status": "Not Started"}
    projects.append(project)

# Function to get project by name
@st.cache(allow_output_mutation=True)
def get_project_by_name(name):
    projects = get_projects()
    for project in projects:
        if project["name"] == name:
            return project
    return None

# Function to add a new task to a project
@st.cache(allow_output_mutation=True)
def add_task(project_name, name, description, deadline, assigned_to):
    tasks = get_tasks()
    projects = get_projects()
    task = {
        "project_name": project_name,
        "name": name,
        "description": description,
        "deadline": deadline,
        "assigned_to": assigned_to,
        "status": "Not Started",
    }
    tasks.append(task)
    for project in projects:
        if project["name"] == project_name:
            project["tasks"].append(task)

# Function to update task status
@st.cache(allow_output_mutation=True)
def update_task_status(task_name, new_status):
    tasks = get_tasks()
    for task in tasks:
        if task["name"] == task_name:
            task["status"] = new_status
            break

# Function to update project status
@st.cache(allow_output_mutation=True)
def update_project_status(project_name, new_status):
    projects = get_projects()
    for project in projects:
        if project["name"] == project_name:
            project["status"] = new_status
            break

# Admin page
def admin_page():
    st.title("Admin Page")

    st.header("User Management")

    # Display existing users
    st.subheader("Existing Users")
    users = get_users()
    for username, user_data in users.items():
        st.write(f"Username: {username}, Role: {user_data['role']}")

    # Add new user
    st.subheader("Add New User")
    new_username = st.text_input("Username", key="new_username")
    new_password = st.text_input("Password", type="password", key="new_password")
    new_role = st.selectbox("Role", ROLES, key="new_role_admin")
    if st.button("Add User"):
        if new_username and new_password and new_role:
            add_user(new_username, new_password, new_role)
            st.success(f"User '{new_username}' added successfully!")
            logging.info(f"User '{new_username}' added successfully!")  # Log successful user addition
        else:
            st.error("Please provide all the user details.")
            logging.error("Incomplete user details provided!")  # Log error for incomplete user details

    # Delete a user
    st.subheader("Delete User")
    delete_username = st.selectbox("Select User", list(users.keys()), key="delete_username")
    if st.button("Delete User"):
        if delete_username:
            delete_user(delete_username)
            st.success(f"User '{delete_username}' deleted successfully!")
        else:
            st.error("Please select a user to delete.")

    # Update user role
    st.subheader("Update User Role")
    update_username = st.selectbox("Select User", list(users.keys()), key="update_username")
    new_role = st.selectbox("New Role", ROLES, key="new_role_update")
    if st.button("Update Role"):
        if update_username and new_role:
            update_user_role(update_username, new_role)
            st.success(f"User '{update_username}' role updated successfully!")
        else:
            st.error("Please select a user and provide a new role.")


# Team Head page
def team_head_page():
    st.title("Team Head Page")

    st.header("Project Management")

    # Create a new project
    st.subheader("Create Project")
    new_project_name = st.text_input("Project Name", key="new_project_name")
    if st.button("Create"):
        if new_project_name:
            create_project(new_project_name)
            st.success(f"Project '{new_project_name}' created successfully!")
            logging.info(f"Project '{new_project_name}' created successfully!")  # Log successful project creation
        else:
            st.error("Please provide a project name.")
            logging.error("Project name not provided!")  # Log error for missing project name

    # View projects
    st.subheader("View Projects")
    projects = get_projects()
    project_name = st.selectbox("Select Project", [project["name"] for project in projects], key="project_name_team_head")
    if st.button("View"):
        if project_name:
            project = get_project_by_name(project_name)
            if project:
                st.write(f"Project Name: {project['name']}")
                st.write(f"Status: {project['status']}")
            else:
                st.error("Project not found.")
        else:
            st.error("Please select a project.")

    # Update project status
        st.subheader("Update Project Status")
    project_name = st.selectbox("Select Project", [project["name"] for project in projects], key="update_project_name")
    new_status = st.selectbox("New Status", ["Not Started", "In Progress", "Completed"], key="new_status")
    if st.button("Update Status"):
        if project_name and new_status:
            update_project_status(project_name, new_status)
            st.success(f"Project '{project_name}' status updated successfully!")
            logging.info(f"Project '{project_name}' status updated successfully!")  # Log successful project status update
        else:
            st.error("Please select a project and provide a new status.")


# Team Member page
def team_member_page():
    st.title("Team Member Page")

    st.header("Task Management")

    # View tasks
    st.subheader("View Tasks")
    tasks = get_tasks()
    task_names = [task["name"] for task in tasks]
    assigned_task = st.selectbox("Select Task", task_names, key="assigned_task")
    if st.button("View"):
        if assigned_task:
            task = [task for task in tasks if task["name"] == assigned_task]
            if task:
                task = task[0]
                st.write(f"Task Name: {task['name']}")
                st.write(f"Project: {task['project_name']}")
                st.write(f"Description: {task['description']}")
                st.write(f"Deadline: {task['deadline']}")
                st.write(f"Status: {task['status']}")
            else:
                st.error("Task not found.")
        else:
            st.error("Please select a task.")

    # Update task status
    st.subheader("Update Task Status")
    task_name = st.selectbox("Select Task", task_names, key="update_task_name")
    new_status = st.selectbox("New Status", ["Not Started", "In Progress", "Completed"], key="new_task_status")
    if st.button("Update Status"):
        if task_name and new_status:
            update_task_status(task_name, new_status)
            st.success(f"Task '{task_name}' status updated successfully!")
            logging.info(f"Task '{task_name}' status updated successfully!")  # Log successful task status update
        else:
            st.error("Please select a task and provide a new status.")


# Login page
def login_page():
    st.title("Project Management System")

    st.header("Login")

    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    role = st.selectbox("Role", ROLES, key="role")

    if st.button("Login"):
        if check_credentials(username, password, role):
            if role == "Admin":
                admin_page()
            elif role == "Team Head":
                team_head_page()
            elif role == "Team Member":
                team_member_page()
        else:
            st.error("Invalid credentials.")
            logging.error("Invalid login attempt!")  # Log invalid login attempt


# Main function
def main():
    login_page()


if __name__ == "__main__":
    main()

