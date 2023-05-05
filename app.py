import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('task_manager.db')
c = conn.cursor()

# Create users table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username text, password text, role text)''')

# Insert default admin user if not exists
c.execute('''INSERT OR IGNORE INTO users (username, password, role)
             VALUES (?, ?, ?)''', ('admin', 'admin123', 'Admin'))

# Insert default team head user if not exists
c.execute('''INSERT OR IGNORE INTO users (username, password, role)
             VALUES (?, ?, ?)''', ('teamhead', 'teamhead123', 'Team Head'))

# Insert default team member user if not exists
c.execute('''INSERT OR IGNORE INTO users (username, password, role)
             VALUES (?, ?, ?)''', ('teammember', 'teammember123', 'Team Member'))

conn.commit()

st.title('Task Manager Login')

username = st.text_input('Username')
password = st.text_input('Password', type='password')

if st.button('Login'):
    # Check if the username and password are correct
    c.execute('''SELECT role FROM users WHERE username = ? AND password = ?''', (username, password))
    result = c.fetchone()
    if result:
        role = result[0]
        st.success(f'Logged in as {role}')

        if role == 'Admin':
            # Show the Admin dashboard
            st.title('Admin Dashboard')

            # Show a table of all the users and their roles
            c.execute('''SELECT username, role FROM users''')
            users = pd.DataFrame(c.fetchall(), columns=['Username', 'Role'])
            st.write(users)

            # Add a new user
            new_username = st.text_input('New Username')
            new_password = st.text_input('New Password', type='password')
            new_role = st.selectbox('New Role', ['Team Head', 'Team Member'])
            if st.button('Add User'):
                c.execute('''INSERT INTO users (username, password, role) VALUES (?, ?, ?)''', (new_username, new_password, new_role))
                conn.commit()
                st.success('User added successfully')
                c.execute('''SELECT username, role FROM users''')
                users = pd.DataFrame(c.fetchall(), columns=['Username', 'Role'])
                st.write(users)

            # Delete a user
            delete_username = st.selectbox('Select User to Delete', users['Username'].tolist())
            if st.button('Delete User'):
                c.execute('''DELETE FROM users WHERE username = ?''', (delete_username,))
                conn.commit()
                st.success('User deleted successfully')
                c.execute('''SELECT username, role FROM users''')
                users = pd.DataFrame(c.fetchall(), columns=['Username', 'Role'])
                st.write(users)

            # Update a user's role
            update_username = st.selectbox('Select User to Update', users['Username'].tolist())
            update_role = st.selectbox('New Role', ['Team Head', 'Team Member'])
            if st.button('Update Role'):
                c.execute('''UPDATE users SET role = ? WHERE username = ?''', (update_role, update_username))
                conn.commit()
                st.success('Role updated successfully')
                c.execute('''SELECT username, role FROM users''')
                users = pd.DataFrame(c.fetchall(), columns=['Username', 'Role'])
                st.write(users)

        elif role == 'Team Head':
            # Show the Team Head dashboard
            st.title('Team Head Dashboard')

            # Create a new project
            project_name = st.text_input('Project Name')
            project_description = st.text_area('Project Description')
            if st.button('Create Project'):
               c.execute('''INSERT INTO projects (name, description) VALUES (?, ?)''', (project_name, project_description))
               conn.commit()
               st.success(f'Project "{project_name}" created successfully')
            
            # Show a list of all the projects
            st.subheader('Projects')
            c.execute('''SELECT name, description FROM projects''')
            projects = pd.DataFrame(c.fetchall(), columns=['Name', 'Description'])
            st.write(projects)

            # Create a new task
            task_project = st.selectbox('Select Project', projects['Name'].tolist())
            task_name = st.text_input('Task Name')
            task_description = st.text_area('Task Description')
            if st.button('Create Task'):
               c.execute('''INSERT INTO tasks (project, name, description) VALUES (?, ?, ?)''', (task_project, task_name, task_description))
               conn.commit()
               st.success(f'Task "{task_name}" created successfully')

            # Show a list of all the tasks
            st.subheader('Tasks')
            c.execute('''SELECT project, name, description FROM tasks''')
            tasks = pd.DataFrame(c.fetchall(), columns=['Project', 'Name', 'Description'])
            st.write(tasks)

        elif role == 'Team Member':
            # Show the Team Member dashboard
            st.title('Team Member Dashboard')

            # Show a list of all the projects
            st.subheader('Projects')
            c.execute('''SELECT name, description FROM projects''')
            projects = pd.DataFrame(c.fetchall(), columns=['Name', 'Description'])
            st.write(projects)

            # Show a list of all the tasks
            st.subheader('Tasks')
            c.execute('''SELECT project, name, description FROM tasks''')
            tasks = pd.DataFrame(c.fetchall(), columns=['Project', 'Name', 'Description'])
            st.write(tasks)

    else:
        st.error('Incorrect username or password')

