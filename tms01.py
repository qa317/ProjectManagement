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

# Function to add a comment/remark to a task
def add_comment(task_name, comment):
    for task in tasks:
        if task["name"] == task_name:
            task["comments"].append(comment)

# Function to add daily progress for a task
def add_progress(task_name, progress):
    for task in tasks:
        if task["name"] == task_name:
            task["progress"].append(progress)

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
    new_role = st.selectbox("Role", ROLES, key="new_role")
    if st.button("Add User"):
        if new_username and new_password and new_role:
            add_user(new_username, new_password, new_role)
            st.success(f"User '{new_username}' added successfully!")
        else:
            st.error("Please provide all the user details.")

    # Delete a user
    st.subheader("Delete User")
    delete_username = st.selectbox("Select User", list(users.keys()),    key="delete_username")
    if st.button("Delete User"):
        if delete_username:
            delete_user(delete_username)
            st.success(f"User '{delete_username}' deleted successfully!")
        else:
            st.error("Please select a user to delete.")

    # Update user role
    st.subheader("Update User Role")
    update_username = st.selectbox("Select User", list(users.keys()), key="update_username")
    new_role = st.selectbox("New Role", ROLES, key="new_role")
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
    st.subheader("Create New Project")
    project_name = st.text_input("Project Name", key="project_name")
    if st.button("Create Project"):
        if project_name:
            create_project(project_name)
            st.success(f"Project '{project_name}' created successfully!")
        else:
            st.error("Please provide a project name.")

    # Add a task to a project
    st.subheader("Add Task to Project")
    project_name = st.selectbox("Select Project", [project["name"] for project in projects], key="project_name")
    task_name = st.text_input("Task Name", key="task_name")
    description = st.text_area("Description", key="description")
    deadline = st.date_input("Deadline", key="deadline")
    assigned_to = st.text_input("Assigned To", key="assigned_to")
    repeat = st.selectbox("Repeat", [None, "Daily", "Weekly"], key="repeat")
    if st.button("Add Task"):
        if project_name and task_name and description and deadline and assigned_to:
            add_task(project_name, task_name, description, deadline, assigned_to, repeat)
            st.success(f"Task '{task_name}' added to project '{project_name}' successfully!")
        else:
            st.error("Please provide all the task details.")

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
    task_name = st.selectbox("Select Task", ["Task 1", "Task 2", "Task 3"], key="task_name")
    status = st.selectbox("Status", ["Not Started", "Started", "Completed", "Cancelled"], key="status")
    if st.button("Update Status"):
        if task_name:
            st.success(f"Task '{task_name}' status updated to '{status}' successfully!")
        else:
            st.error("Please select a task.")

    # Add comment/remark for a task
    st.subheader("Add Comment / Remark")
    task_name = st.selectbox("Select Task", ["Task 1", "Task 2", "Task 3"], key="task_name")
    comment = st.text_area("Comment", key="comment")
    if st.button("Add Comment"):
        if task_name and comment:
            add_comment(task_name, comment)
            st.success(f"Comment added to task '{task_name}' successfully!")
        else:
            st.error("Please select a task and provide a comment.")

    # Add daily progress for a task
    st.subheader("Add Daily Progress")
    task_name = st.selectbox("Select Task", ["Task 1", "Task 2", "Task 3"], key="task_name")
    progress = st.text_input("Daily Progress", key="progress")
    if st.button("Add Progress"):
        if task_name and progress:
            add_progress(task_name, progress)
            st.success(f"Daily progress added to task '{task_name}' successfully!")
        else:
            st.error("Please select a task and provide daily progress.")

# Main function
def main():
    st.sidebar.title("Task Manager")
    page = st.sidebar.radio("Navigation", ["Admin", "Team Head", "Team Member"])

    if page == "Admin":
        login_page("Admin")
    elif page == "Team Head":
        login_page("Team Head")
    elif page == "Team Member":
        login_page("Team Member")


# Login page
def login_page(role):
    st.title(f"{role} Login")

    username = st.text_input("Username", key=f"{role}_username")
    password = st.text_input("Password", type="password", key=f"{role}_password")

    if st.button("Login"):
        if check_credentials(username, password, role):
            if role == "Admin":
                admin_page()
            elif role == "Team Head":
                team_head_page()
            elif role == "Team Member":
                team_member_page()
        else:
            st.error("Invalid username or password.")


if __name__ == "__main__":
    main()


