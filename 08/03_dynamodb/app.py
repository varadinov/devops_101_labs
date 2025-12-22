import streamlit as st
from dynamodb_utils import (
    table_exists, put_item, get_all_items,
    update_item, delete_item
)

st.set_page_config(page_title="DynamoDB Task Manager", layout="wide")

st.title("📋 DynamoDB Task Manager")

# Load table name from Streamlit secrets
try:
    table_name = st.secrets["table_name"]
    if not table_name or table_name == "your-table-name-here":
        st.error("⚠️ Please configure the table name in .streamlit/secrets.toml")
        st.stop()
except KeyError:
    st.error("⚠️ 'table_name' not found in .streamlit/secrets.toml. Please add it.")
    st.stop()

# Check if table exists
if not table_exists(table_name):
    st.error(f"❌ Table '{table_name}' does not exist. Please create it first using the AWS CLI (see readme.md for instructions).")
    st.stop()

st.info(f"📊 Connected to table: **{table_name}**")

# Sidebar for adding new tasks
with st.sidebar:
    st.header("➕ Add New Task")
    
    with st.form("add_task_form"):
        task_title = st.text_input("Task Title", placeholder="Enter task title...")
        task_description = st.text_area("Description", placeholder="Enter task description (optional)...")
        task_status = st.selectbox("Status", ["pending", "in_progress", "completed"])
        
        submitted = st.form_submit_button("Add Task", type="primary")
        
        if submitted:
            if task_title:
                task_id = put_item(table_name, task_title, task_description, task_status)
                if task_id:
                    st.success(f"✅ Task added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add task. Check your AWS credentials.")
            else:
                st.warning("⚠️ Please enter a task title.")

# Main area for displaying tasks
st.header("📝 Your Tasks")

if st.button("🔄 Refresh List"):
    st.rerun()

tasks = get_all_items(table_name)

if not tasks:
    st.info("No tasks found. Add a new task using the sidebar!")
else:
    st.write(f"Found {len(tasks)} task(s)")
    
    # Group tasks by status
    pending_tasks = [t for t in tasks if t.get('status') == 'pending']
    in_progress_tasks = [t for t in tasks if t.get('status') == 'in_progress']
    completed_tasks = [t for t in tasks if t.get('status') == 'completed']
    
    # Create tabs for different statuses
    tab1, tab2, tab3 = st.tabs(["⏳ Pending", "🔄 In Progress", "✅ Completed"])
    
    def display_task(task):
        """Display a single task with edit and delete options."""
        task_id = task['task_id']
        title = task.get('title', 'Untitled')
        description = task.get('description', '')
        status = task.get('status', 'pending')
        created_at = task.get('created_at', '')
        
        with st.container():
            st.subheader(title)
            if description:
                st.write(description)
            st.caption(f"Created: {created_at}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Status update buttons
                if status == 'pending':
                    if st.button("▶️ Start", key=f"start_{task_id}"):
                        if update_item(table_name, task_id, status='in_progress'):
                            st.success("Task started!")
                            st.rerun()
                elif status == 'in_progress':
                    if st.button("✅ Complete", key=f"complete_{task_id}"):
                        if update_item(table_name, task_id, status='completed'):
                            st.success("Task completed!")
                            st.rerun()
            
            with col2:
                # Edit button
                if st.button("✏️ Edit", key=f"edit_{task_id}"):
                    st.session_state[f'editing_{task_id}'] = True
            
            with col3:
                # Delete button
                if st.button("🗑️ Delete", key=f"delete_{task_id}"):
                    if delete_item(table_name, task_id):
                        st.success("Task deleted!")
                        st.rerun()
                    else:
                        st.error("Failed to delete task")
            
            # Edit form (shown when edit button is clicked)
            if st.session_state.get(f'editing_{task_id}', False):
                with st.form(f"edit_form_{task_id}"):
                    new_title = st.text_input("Title", value=title, key=f"title_{task_id}")
                    new_description = st.text_area("Description", value=description, key=f"desc_{task_id}")
                    new_status = st.selectbox(
                        "Status",
                        ["pending", "in_progress", "completed"],
                        index=["pending", "in_progress", "completed"].index(status),
                        key=f"status_{task_id}"
                    )
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.form_submit_button("💾 Save"):
                            if update_item(table_name, task_id, new_title, new_description, new_status):
                                st.session_state[f'editing_{task_id}'] = False
                                st.success("Task updated!")
                                st.rerun()
                    with col_cancel:
                        if st.form_submit_button("❌ Cancel"):
                            st.session_state[f'editing_{task_id}'] = False
                            st.rerun()
            
            st.divider()
    
    # Display tasks in their respective tabs
    with tab1:
        if pending_tasks:
            for task in pending_tasks:
                display_task(task)
        else:
            st.info("No pending tasks.")
    
    with tab2:
        if in_progress_tasks:
            for task in in_progress_tasks:
                display_task(task)
        else:
            st.info("No tasks in progress.")
    
    with tab3:
        if completed_tasks:
            for task in completed_tasks:
                display_task(task)
        else:
            st.info("No completed tasks.")

