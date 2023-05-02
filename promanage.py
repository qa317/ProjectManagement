import streamlit as st

# Create new project page
def create_new_project():
    st.header("Create New Project")
    project_name = st.text_input("Project Name")
    task = st.text_input("Task")
    description = st.text_input("Description")
    task_deadline = st.date_input("Task Deadline")
    priority_level = st.selectbox("Priority Level", ["High", "Medium", "Low"])
    team_members = st.multiselect("Team Members", ["Alice", "Bob", "Charlie", "David"])
    if st.button("Create Project"):
        # Save the project data to the database
        # TODO: add database code here
        st.success("Project created successfully")

# Create individual tasks page
def create_individual_tasks():
    st.header("Create Individual Tasks")
    task_name = st.text_input("Task Name")
    task_description = st.text_input("Task Description")
    task_deadline = st.date_input("Task Deadline")
    priority_level = st.selectbox("Priority Level", ["High", "Medium", "Low"])
    repeat_frequency = st.selectbox("Repeat Frequency", ["Daily", "Weekly", "Monthly", "Never"])
    team_members = st.multiselect("Team Members", ["Alice", "Bob", "Charlie", "David"])
    if st.button("Create Task"):
        # Save the task data to the database
        # TODO: add database code here
        st.success("Task created successfully")

# Define the pages
pages = {
    "Create New Project": create_new_project,
    "Create Individual Tasks": create_individual_tasks,
}

# App title and sidebar navigation
st.set_page_config(page_title="Project Manager", page_icon=":clipboard:", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Pages", list(pages.keys()))

# Display the selected page
pages[page]()
