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
users = {
    admin_username: {"password": admin_password, "role": "Admin"},
    team_head_username: {"password": team_head_password, "role": "Team Head"},
    team_member_username: {"password": team_member_password, "role": "Team Member"},
}

# Project storage
projects = []

# Task storage
tasks = []

# Function to check user credentials
def check_credentials(username, password, role):
    user = users.get(username)
    if user and user["password"] == password and user["role"] == role:
        return True
    return False

# Function to add a new user
def add_user(username, password, role):
    users[username] = {"password": password, "role": role}

# Function to delete a user
def delete_user(username):
    if username in users:
        del users[username]

# Function to update a user's role
def update_user_role(username, new_role):
    if username in users:
        users[username]["role"] = new_role

# Function to create a new project
def create_project(name):
    project = {
        "name": name,
        "tasks": [],
        "start_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "end_date": (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
        "status": "Not Started",
    }
    projects.append(project)

# Function to get project by name
def get_project_by_name(name):
    for project in projects:
        if project["name"] == name:
            return project
    return None

# Function to add a new task to a project
def add_task(project_name, name, description, deadline, assigned_to):
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
def update_task_status(task_name, new_status):
    for task in tasks:
        if task["name"] == task_name:
            task["status"] = new_status
            break

def update_project_status(project_name, new_status):
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
    project_name = st.selectbox("Select Project", [project["name"] for project in projects], key="project_name_team_head")
    if st.button("View"):
        if project_name:
            project = get_project_by_name(project_name)
            if project:
                st.write(f"Project Name: {project['name']}")
                st.write(f"Start Date: {project['start_date']}")
                st.write(f"End Date: {project['end_date']}")
                st.write(f"Status: {project['status']}")
            else:
                st.error("Project not found.")
        else:
            st.error("Please select a project.")

    # Update project status
    st.subheader("Update Project Status")
    update_project_name = st.selectbox("Select Project", [project["name"] for project in projects], key="update_project_name")
    new_status = st.selectbox("New Status", ["Not Started", "In Progress", "Completed"], key="new_status_team_head")
    if st.button("Update"):
        if update_project_name and new_status:
            update_project_status(update_project_name, new_status)
            st.success(f"Project '{update_project_name}' status updated successfully!")
        else:
            st.error("Please select a project and provide a new status.")


# Team Member page
def team_member_page():
    st.title("Team Member Page")

    st.header("Task Management")

    # Punch in - punch out
    st.subheader("Punch In - Punch Out")
    punch_in_out = st.button("Punch In / Out")

    if punch_in_out:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        st.success(f"Punched {'In' if punch_in_out else 'Out'} at {current_time}.")
        logging.info(f"Punched {'In' if punch_in_out else 'Out'} at {current_time}.")  # Log punch in/out event

    # View Dashboard
    st.subheader("Dashboard")
    st.write("Total assigned tasks:")
    st.write("Completed tasks:")
    st.write("Details about timely completion of tasks:")
    st.write("Upcoming deadlines:")

    # Check individual assigned tasks
    st.subheader("Assigned Tasks")
    st.write("Task 1")
    st.write("Task 2")
    st.write("Task 3")

    # Change task status
    st.subheader("Change Task Status")
    task_name = st.selectbox("Select Task", ["Task 1", "Task 2", "Task 3"], key="task_name_team_member")
    new_status = st.selectbox("New Status", ["Not Started", "In Progress", "Completed"], key="new_status_team_member")
    if st.button("Update"): 
        if task_name and new_status:
            update_task_status(task_name, new_status)
            st.success(f"Task '{task_name}' status updated successfully!")
        else:
            st.error("Please select a task and provide a new status.")

# Main application
def main():
    st.sidebar.title("User Login")

    # Login credentials
    username = st.sidebar.text_input("Username", key="username")
    password = st.sidebar.text_input("Password", type="password", key="password")
    role = st.sidebar.selectbox("Role", ROLES, key="role")

    if st.sidebar.button("Login"):
        if check_credentials(username, password, role):
            st.sidebar.success("Logged in successfully!")
            logging.info("Logged in successfully!")  # Log successful login
            if role == "Admin":
                admin_page()
            elif role == "Team Head":
                team_head_page()
            elif role == "Team Member":
                team_member_page()
        else:
            st.sidebar.error("Invalid username or password.")
            logging.error("Invalid username or password!")  # Log login failure

if __name__ == "__main__":
    main()





