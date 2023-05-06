import streamlit as st
import datetime

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
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    new_role = st.selectbox("Role", ROLES)
    if st.button("Add User"):
        if new_username and new_password and new_role:
            add_user(new_username, new_password, new_role)
            st.success("User added successfully!")
        else:
            st.error("Please fill in all the fields.")

    # Delete user
    st.subheader("Delete User")
    delete_username = st.selectbox("Select User", list(users.keys()))
    if st.button("Delete User"):
        if delete_username:
            delete_user(delete_username)
            st.success("User deleted successfully!")
        else:
            st.error("Please select a user to delete.")

    # Update user role
    st.subheader("Update User Role")
    update_username = st.selectbox("Select User", list(users.keys()))
    new_role = st.selectbox("New Role", ROLES)
    if st.button("Update Role"):
        if update_username and new_role:
            update_user_role(update_username, new_role)
            st.success("User role updated successfully!")
        else:
            st.error("Please select a user and choose a new role.")

# Function to create a new project
def create_project(name):
    project = {"name": name, "tasks": []}
    projects.append(project)

# Function to add a new task to a project
def add_task(project_name, name, description, deadline, assigned_to, repeat=None):
    task = {
        "project_name": project_name,
        "name": name,
        "description": description,
        "deadline": deadline,
        "assigned_to": assigned_to,
        "status": "Not Started",
        "repeat": repeat,
        "comments": [],
        "progress": [],
    }
    tasks.append(task)
    for project in projects:
        if project["name"] == project_name:
            project["tasks"].append(task)

# Team Head page
def team_head_page():
    st.title("Team Head Page")

    # Create new project
    st.header("Create New Project")
    new_project_name = st.text_input("Project Name")
    if st.button("Create Project"):
        if new_project_name:
            create_project(new_project_name)
            st.success("Project created successfully!")
        else:
            st.error("Please enter a project name.")

    # Add new task
    st.header("Add Task")
    project_names = [project["name"] for project in projects]
    new_task_project = st.selectbox("Select Project", project_names)
    new_task_name = st.text_input("Task Name")
    new_task_description = st.text_area("Task Description")
    new_task_deadline = st.date_input("Task Deadline", value=datetime.date.today())
    new_task_assigned_to = st.selectbox("Assign Task to", list(users.keys()))
    new_task_repeat = st.selectbox("Repeat Task", ["Daily", "Weekly", None])
    if st.button("Add Task"):
        if new_task_project and new_task_name and new_task_description and new_task_assigned_to:
            add_task(
                new_task_project,
                new_task_name,
                new_task_description,
                new_task_deadline,
                new_task_assigned_to,
                new_task_repeat,
            )
            st.success("Task added successfully!")
        else:
            st.error("Please fill in all the fields.")

    # Display tasks
    st.header("Tasks")
    for project in projects:
        st.subheader(project["name"])
        for task in project["tasks"]:
            if task["assigned_to"] == team_head_username:
                st.write(f"Task Name: {task['name']}")
                st.write(f"Description: {task['description']}")
                st.write(f"Deadline: {task['deadline']}")
                st.write(f"Assigned to: {task['assigned_to']}")
                st.write(f"Status: {task['status']}")
                st.write(f"Repeat: {task['repeat']}")
                st.write("---")

# Function to add a comment/remark to a task
def add_comment(task_name, comment):
    for task in tasks:
        if task["name"] == task_name:
            task["comments"].append(comment)
            break

# Team Member page
def team_member_page():
    st.title("Team Member Page")

    # Display assigned tasks
    st.header("Assigned Tasks")
    for task in tasks:
        if task["assigned_to"] == team_member_username:
            st.write(f"Task Name: {task['name']}")
            st.write(f"Description: {task['description']}")
            st.write(f"Deadline: {task['deadline']}")
            st.write(f"Assigned to: {task['assigned_to']}")
            st.write(f"Status: {task['status']}")
            st.write(f"Repeat: {task['repeat']}")
            st.write("---")

    # Update task status
    st.header("Update Task Status")
    task_names = [task["name"] for task in tasks if task["assigned_to"] == team_member_username]
    selected_task = st.selectbox("Select Task", task_names)
    new_status = st.selectbox("New Status", ["Not Started", "In Progress", "Completed"])
    if st.button("Update Status"):
        if selected_task and new_status:
            for task in tasks:
                if task["name"] == selected_task and task["assigned_to"] == team_member_username:
                    task["status"] = new_status
                    st.success("Task status updated successfully!")
                    break

    # Add comment/remark to a task
    st.header("Add Comment to Task")
    comment_task = st.selectbox("Select Task", task_names)
    new_comment = st.text_input("Comment")
    if st.button("Add Comment"):
        if comment_task and new_comment:
            add_comment(comment_task, new_comment)
            st.success("Comment added successfully!")
        else:
            st.error("Please select a task and enter a comment.")

# Login page
def login_page():
    st.title("Task Management System")

    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ROLES)

    if st.button("Login"):
        if check_credentials(username, password, role):
            st.success(f"Welcome, {username}!")
            if role == "Admin":
                admin_page()
            elif role == "Team Head":
                team_head_page()
            elif role == "Team Member":
                team_member_page()
        else:
            st.error("Invalid credentials. Please try again.")

# Main function
def main():
    login_page()

if __name__ == "__main__":
    main()


