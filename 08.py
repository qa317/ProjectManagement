pip install flask
import streamlit as st
import pandas as pd
import sqlite3
import os
from flask import Flask, make_response, request

# Remove the existing database file
if os.path.exists('task_manager.db'):
    os.remove('task_manager.db')

# Create a new database file
conn = sqlite3.connect('task_manager.db')
cursor = conn.cursor()


# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
''')

# Create the projects table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        status TEXT
    )
''')

# Create the tasks table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        name TEXT,
        description TEXT,
        deadline TEXT,
        status TEXT,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    )
''')

# Create the comments table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        text TEXT,
        FOREIGN KEY (task_id) REFERENCES tasks (id)
    )
''')

# Initialize Flask app
app = Flask(__name__)

# Set a secret key for secure cookie encoding
app.secret_key = "admin09"
# Function to retrieve session data from cookies
def get_session_data():
    session_id = request.cookies.get("session_id")
    session_data = request.cookies.get("session_data")

    if session_id is None or session_data is None:
        # No session data found, create a new session
        session_id = "session1"
        session_data = {"username": "", "role": ""}
    else:
        # Parse session data from string to dictionary
        session_data = eval(session_data)

    return session_id, session_data

# Function to store session data in cookies
def store_session_data(session_id, session_data):
    # Convert session data dictionary to string
    session_data_str = str(session_data)

    # Store session data in cookies
    response = make_response()
    response.set_cookie("session_id", session_id)
    response.set_cookie("session_data", session_data_str)

    return response
# Function to add a user to the database
def add_user(username, password, role):
    cursor.execute('''
        INSERT INTO users (username, password, role) VALUES (?, ?, ?)
    ''', (username, password, role))
    conn.commit()

# Function to retrieve a user from the database by username
def get_user(username):
    cursor.execute('''
        SELECT * FROM users WHERE username=?
    ''', (username,))
    return cursor.fetchone()

# Function to update a user's role in the database
def update_user_role(username, role):
    cursor.execute('''
        UPDATE users SET role=? WHERE username=?
    ''', (role, username))
    conn.commit()

# Function to add a project to the database
def add_project(name, status):
    cursor.execute('''
        INSERT INTO projects (name, status) VALUES (?, ?)
    ''', (name, status))
    conn.commit()

# Function to retrieve all projects from the database
def get_all_projects():
    cursor.execute('''
        SELECT * FROM projects
    ''')
    return cursor.fetchall()

# Function to add a task to the database
def add_task(project_id, name, description, deadline, status):
    cursor.execute('''
        INSERT INTO tasks (project_id, name, description, deadline, status) VALUES (?, ?, ?, ?, ?)
    ''', (project_id, name, description, deadline, status))
    conn.commit()

# Function to retrieve all tasks for a given project from the database
def get_tasks_by_project(project_id):
    cursor.execute('''
        SELECT * FROM tasks WHERE project_id=?
    ''', (project_id,))
    return cursor.fetchall()

# Function to add a comment to the database
def add_comment(task_id, text):
    cursor.execute('''
        INSERT INTO comments (task_id, text) VALUES (?, ?)
    ''', (task_id, text))
    conn.commit()

# Function to retrieve all comments for a given task from the database
def get_comments_by_task(task_id):
    cursor.execute('''
        SELECT * FROM comments WHERE task_id=?
    ''', (task_id,))
    return cursor.fetchall()

# Function to check the credentials of a user
def check_credentials(username, password):
    user = get_user(username)
    if user is not None:
        if user[2] == password:
            return True
    return False

# Function to get the role of a user
def get_user_role(username):
    user = get_user(username)
    if user is not None:
        return user[3]
    return None

# Function to get all users from the database
def get_all_users():
    cursor.execute('''
        SELECT username, role FROM users
    ''')
    return cursor.fetchall()

# Function to delete a user from the database
def delete_user(username):
    cursor.execute('''
        DELETE FROM users WHERE username=?
    ''', (username,))
    conn.commit()

# Function to create a project
def create_project(name, username):
    add_project(name, 'Active')

# Function to create a task
def create_task(name, description, deadline, repeat, team_members, username):
    # Retrieve the project ID based on the project name
    project_id = get_project_id_by_name(name)

    # Add the task to the database
    add_task(project_id, name, description, deadline, 'Pending')

# Function to get the project ID based on the project name
def get_project_id_by_name(name):
    cursor.execute('''
        SELECT id FROM projects WHERE name=?
    ''', (name,))
    result = cursor.fetchone()
    if result is not None:
        return result[0]
    return None

# Function to get team members for a specific user
def get_team_members(username):
    cursor.execute('''
        SELECT username FROM users WHERE role='Team Member' AND username!=?
    ''', (username,))
    return [member[0] for member in cursor.fetchall()]

# Function to get assigned tasks for a specific user
def get_assigned_tasks(username):
    cursor.execute('''
        SELECT t.name AS task_name, t.status
        FROM tasks AS t
        INNER JOIN projects AS p ON t.project_id = p.id
        WHERE p.name IN (
            SELECT name FROM projects WHERE status='Active'
        ) AND ? IN (
            SELECT username FROM users WHERE role='Team Member'
        )
    ''', (username,))
    return cursor.fetchall()

# Function to update the status of a task
def update_task_status(task_name, status):
    cursor.execute('''
        UPDATE tasks SET status=? WHERE name=?
    ''', (status, task_name))
    conn.commit()

# Function to add a comment to a task
def add_task_comment(task_name, comment_text, username):
    # Retrieve the task ID based on the task name
    task_id = get_task_id_by_name(task_name)

    # Add the comment to the database
    add_comment(task_id, comment_text)

# Function to get the task ID based on the task name
def get_task_id_by_name(name):
    cursor.execute('''
        SELECT id FROM tasks WHERE name=?
    ''', (name,))
    result = cursor.fetchone()
    if result is not None:
        return result[0]
    return None

# Main program
def main():
    conn = sqlite3.connect('task_manager.db')
    st.title('Task Manager')

    # Check if the default admin user exists, if not, add it
    if get_user('admin') is None:
        add_user('admin', 'admin@123#', 'Admin')
        st.success('Default admin user added successfully')
    
    # Check if the default team head user exists, if not, add it
    if get_user('teamhead') is None:
        add_user('teamhead', 'head@123#', 'Team Head')
        st.success('Default team head user added successfully')

    # Check if the default team member user exists, if not, add it
    if get_user('teammember') is None:
        add_user('teammember', 'member@123#', 'Team Member')
        st.success('Default team member user added successfully')
    # Retrieve session data from cookies
    session_id, session_data = get_session_data()


    # Login
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        # Check if the username and password are correct
        if check_credentials(username, password):
            st.success(f'Logged in as {username}')

            # Get the user's role
            role = get_user_role(username)
            session_data["username"] = username
            session_data["role"] = role
            
            # Store updated session data in cookies
            return store_session_data(session_id, session_data)
        else:
            st.error('Invalid username or password')

            if role == 'Admin':
                render_admin_dashboard()
            elif role == 'Team Head':
                render_team_head_dashboard(username)
            elif role == 'Team Member':
                render_team_member_dashboard(username)
            else:
                st.error('Invalid user role')
    else:
        st.error('Invalid username or password')

# Global cache variable
cache = {}

# Render the Admin dashboard
def render_admin_dashboard():
    if 'admin_dashboard' not in cache:
        st.subheader('Admin Dashboard')

    # Show a table of all the users and their roles
    users = get_all_users()
    user_table = pd.DataFrame(users, columns=['Username', 'Role'])
    st.write(user_table)

    # Add a new user
    new_username = st.text_input('New Username')
    new_password = st.text_input('New Password', type='password')
    new_role = st.selectbox('New Role', ['Team Head', 'Team Member'], key='new_user_role')
    if st.button('Add User'):
        add_user(new_username, new_password, new_role)
        st.success('User added successfully')
        st.experimental_rerun()

    # Delete a user
    delete_username = st.selectbox('Select User to Delete', [user[0] for user in users], key='delete_user')
    if st.button('Delete User'):
        delete_user(delete_username)
        st.success('User deleted successfully')
        st.experimental_rerun()

    # Update a user's role
    update_username = st.selectbox('Select User to Update', [user[0] for user in users], key='update_username')
    update_role = st.selectbox('New Role', ['Team Head', 'Team Member'], key='update_user_role')
    if st.button('Update Role'):
        update_user_role(update_username, update_role)
        st.success('Role updated successfully')
        st.experimental_rerun()
    cache['admin_dashboard'] = True


# Render the Team Head dashboard
def render_team_head_dashboard(username):
    if 'team_head_dashboard' not in cache:
        st.subheader(f'Team Head Dashboard ({username})')

    # Create a new project
    project_name = st.text_input('Project Name')
    if st.button('Create Project'):
        create_project(project_name, username)
        st.success(f'Project "{project_name}" created successfully')
        st.experimental_rerun()

    # Create a new task
    task_name = st.text_input('Task Name')
    task_description = st.text_area('Task Description')
    task_deadline = st.date_input('Task Deadline')
    team_members = st.multiselect('Team Members', get_team_members(username))
    if st.button('Create Task'):
        create_task(task_name, task_description, task_deadline, team_members, username)
        st.success('Task created successfully')
        st.experimental_rerun()
        
        cache['team_head_dashboard'] = True

# Render the Team Member dashboard
def render_team_member_dashboard(username):
    if 'team_member_dashboard' not in cache:
        st.subheader(f'Team Member Dashboard ({username})')

    # View your assigned tasks
    tasks = get_assigned_tasks(username)
    st.write(pd.DataFrame(tasks, columns=['Task Name', 'Status']))

    # Update a task's status
    update_task = st.selectbox('Select Task to Update', [task['task_name'] for task in tasks])
    update_status = st.selectbox('New Status', ['Pending', 'In Progress', 'Completed', 'Cancelled'])
    if st.button('Update Status'):
        update_task_status(update_task, update_status)
        st.success('Task status updated successfully')
        st.experimental_rerun()

    # Add a comment to a task
    comment_task = st.selectbox('Select Task to Comment', [task['task_name'] for task in tasks])
    comment_text = st.text_area('Comment')
    if st.button('Add Comment'):
        add_task_comment(comment_task, comment_text, username)
        st.success('Comment added successfully')
        st.experimental_rerun()
        
        cache['team_member_dashboard'] = True
               
# Run the main program
@app.route('/')
def run_app():
    return main()

if __name__ == '__main__':
    app.run()


