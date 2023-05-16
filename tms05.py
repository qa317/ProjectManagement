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
@st.cache_data(persist=True)
def get_users():
    return {
        admin_username: {"password": admin_password, "role": "Admin"},
        team_head_username: {"password": team_head_password, "role": "Team Head"},
        team_member_username: {"password": team_member_password, "role": "Team Member"},
    }

# Project storage
@st.cache_data(persist=True)
def get_projects():
    return []

# Task storage
@st.cache_data(persist=True)
def get_tasks():
    return []

# Function to check user credentials
def check_credentials(username, password, role):
    users = get_users()
    user = users.get(username)
    if user and user["password"] == password and user["role"] == role:
        return True
    return False

# Function to add a new user
@st.cache_data(persist=True)
def add_user(username, password, role):
    users = get_users()
    users[username] = {"password": password, "role": role}

# Function to delete a user
@st.cache_data(persist=True)
def delete_user(username):
    users = get_users()
    if username in users:
        del users[username]

# Function to update a user's role
@st.cache_data(persist=True)
def update_user_role(username, new_role):
    users = get_users()
    if username in users:
        users[username]["role"] = new_role

# Function to create a new project
@st.cache_data(persist=True)
def create_project(name):
    projects = get_projects()
    project = {"name": name, "tasks": [], "status": "Not Started"}
    projects.append(project)

# Function to get project by name
@st.cache_data(persist=True)
def get_project_by_name(name):
    projects = get_projects()
    for project in projects:
        if project["name"] == name:
            return project
    return None

# Function to add a new task to a project
@st.cache_data(persist=True)
def add_task(project_name, name, description, deadline, assigned_to):
    projects = get_projects()
    tasks = get_tasks()
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
@st.cache_data(persist=True)
def update_task_status(task_name, new_status):
    tasks = get_tasks()
    for task in tasks:
        if task["name"] == task_name:
            task["status"] = new_status
            break

# Function to update project status
@st.cache_data(persist=True)
def update_project_status(project_name, new_status):
    projects = get_projects()
    for project in projects:
        if project["name"] == project_name:
            project["status"] = new_status
            break

# Main program
def main():
    st.title("Project Management System")

    # Login
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ROLES)

    if st.button("Login"):
        if check_credentials(username, password, role):
            st.success("Logged in successfully!")
            st.experimental_singleton("current_user")
            st.experimental_singleton("current_role", role)
            st.experimental_rerun()
        else:
            st.error("Invalid username, password, or role!")

    # User actions
    if "current_user" in st.experimental_get_query_params().keys():
        current_user = st.experimental_singleton("current_user")
        current_role = st.experimental_singleton("current_role")

        if current_role == "Admin":
            st.subheader("Admin Panel")
            action = st.selectbox("Select action", ["Add User", "Delete User", "Update User Role"])

            if action == "Add User":
                st.subheader("Add User")
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                new_role = st.selectbox("Role", ROLES)
                if st.button("Add"):
                    add_user(new_username, new_password, new_role)
                    st.success("User added successfully!")

            elif action == "Delete User":
                st.subheader("Delete User")
                users = get_users()
                usernames = list(users.keys())
                selected_username = st.selectbox("Select user to delete", usernames)
                if st.button("Delete"):
                    delete_user(selected_username)
                    st.success("User deleted successfully!")

            elif action == "Update User Role":
                st.subheader("Update User Role")
                users = get_users()
                usernames = list(users.keys())
                selected_username = st.selectbox("Select user to update", usernames)
                new_role = st.selectbox("New role", ROLES)
                if st.button("Update"):
                    update_user_role(selected_username, new_role)
                    st.success("User role updated successfully!")

        elif current_role == "Team Head":
            st.subheader("Team Head Panel")
            action = st.selectbox("Select action", ["Create Project"])

            if action == "Create Project":
                st.subheader("Create Project")
                project_name = st.text_input("Project Name")
                if st.button("Create"):
                    create_project(project_name)
                    st.success("Project created successfully!")

        elif current_role == "Team Member":
            st.subheader("Team Member Panel")
            action = st.selectbox("Select action", ["View Projects", "View Tasks"])

            if action == "View Projects":
                st.subheader("View Projects")
                projects = get_projects()
                project_names = [project["name"] for project in projects]
                selected_project = st.selectbox("Select project", project_names)
                project = get_project_by_name(selected_project)
                st.write("Project Name:", project["name"])
                st.write("Status:", project["status"])

            elif action == "View Tasks":
                st.subheader("View Tasks")
                tasks = get_tasks()
                filtered_tasks = [task for task in tasks if task["assigned_to"] == current_user]
                for task in filtered_tasks:
                    st.write("Task Name:", task["name"])
                    st.write("Project Name:", task["project_name"])
                    st.write("Status:", task["status"])

    # Logout
    if st.button("Logout"):
        st.experimental_rerun()


if __name__ == "__main__":
    main()


