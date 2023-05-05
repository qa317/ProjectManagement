import streamlit as st
import pandas as pd

st.title('Task Manager Login')

username = st.text_input('Username')
password = st.text_input('Password', type='password')

if st.button('Login'):
    # Check if the username and password are correct
    if username == 'admin' and password == 'admin123':
        st.success('Logged in as Admin')
        # Show the Admin dashboard
    elif username == 'teamhead' and password == 'teamhead123':
        st.success('Logged in as Team Head')
        # Show the Team Head dashboard
    elif username == 'teammember' and password == 'teammember123':
        st.success('Logged in as Team Member')
        # Show the Team Member dashboard
    else:
        st.error('Invalid username or password')

if username == 'admin' and password == 'admin123':
    st.title('Admin Dashboard')

    # Show a table of all the users and their roles
    users = pd.DataFrame({'Username': ['teamhead', 'teammember'], 'Role': ['Team Head', 'Team Member']})
    st.write(users)

    # Add a new user
    new_username = st.text_input('New Username')
    new_password = st.text_input('New Password', type='password')
    new_role = st.selectbox('New Role', ['Team Head', 'Team Member'])
    if st.button('Add User'):
        users = users.append({'Username': new_username, 'Role': new_role}, ignore_index=True)
        st.success('User added successfully')
        st.write(users)

    # Delete a user
    delete_username = st.selectbox('Select User to Delete', users['Username'].tolist())
    if st.button('Delete User'):
        users = users[users['Username'] != delete_username]
        st.success('User deleted successfully')
        st.write(users)

    # Update a user's role
    update_username = st.selectbox('Select User to Update', users['Username'].tolist())
    update_role = st.selectbox('New Role', ['Team Head', 'Team Member'])
    if st.button('Update Role'):
        users.loc[users['Username'] == update_username, 'Role'] = update_role
        st.success('Role updated successfully')
        st.write(users)
if username == 'teamhead' and password == 'teamhead123':
    st.title('Team Head Dashboard')

    # Create a new project
    project_name = st.text_input('Project Name')
    if st.button('Create Project'):
        st.success(f'Project "{project_name}" created successfully')

    # Create a new task
    task_name = st.text_input('Task Name')
    task_description = st.text_area('Task Description')
    task_deadline = st.date_input('Task Deadline')
    task_repeat = st.selectbox('Repeat Task', ['Daily', 'Weekly', 'No'])
    team_members = st.multiselect('Team Members', ['Alice', 'Bob', 'Charlie'])
    if st.button('Create Task'):
    # Save the task details to a database or file
     st.success('Task created successfully')

if username == 'teammember' and password == 'teammember123':
    st.title('Team Member Dashboard')

    # Punch in - punch out
    if st.button('Punch In'):
        st.success('You are now punched in')
    if st.button('Punch Out'):
        st.success('You are now punched out')

    # View your assigned tasks
    tasks = pd.DataFrame({'Task Name': ['Task 1', 'Task 2'], 'Status': ['Pending', 'Completed']})
    st.write(tasks)

    # Update a task's status
    update_task = st.selectbox('Select Task to Update', tasks['Task Name'].tolist())
    update_status = st.selectbox('New Status', ['Pending', 'In Progress', 'Completed', 'Cancelled'])
    if st.button('Update Status'):
        tasks.loc[tasks['Task Name'] == update_task, 'Status'] = update_status
        st.success('Status updated successfully')
        st.write(tasks)

    # Add a comment or remark for a task
    comment_task = st.selectbox('Select Task to Add Comment', tasks['Task Name'].tolist())
    comment_text = st.text_input('Comment')
    if st.button('Add Comment'):
        # Save the comment to a database or file
        st.success('Comment added successfully')

