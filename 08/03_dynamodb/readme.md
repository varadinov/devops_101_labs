# DynamoDB Demo

This demo shows how to use Amazon DynamoDB to create, read, update, and delete items in a NoSQL database. You'll build a simple task manager application that demonstrates core DynamoDB operations.

## Setup

### 1. Create DynamoDB Table

First, create a DynamoDB table using the AWS CLI:

```bash
export AWS_PROFILE=demo
aws dynamodb create-table \
  --table-name my-demo-tasks-22122025 \
  --attribute-definitions AttributeName=task_id,AttributeType=S \
  --key-schema AttributeName=task_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

The command will create a new DynamoDB table with:
- **Partition Key**: `task_id` (String)
- **Billing Mode**: Pay-per-request (on-demand pricing)

**List tables (if needed):**

```bash
aws dynamodb list-tables --region us-east-1
```

### 2. Configure Streamlit Secrets

Create or update the secrets file for the Streamlit app:

```bash
mkdir -p .streamlit
echo 'table_name = "my-demo-tasks-22122025"' >> .streamlit/secrets.toml
```

If you already have a `secrets.toml` file from previous demos, you can add the `table_name` line to it.

### 3. Run the Application

Start the Streamlit app:

```bash
uv run streamlit run app.py
```

The app will open in your browser. You can:
- Add new tasks with title, description, and status
- View tasks organized by status (Pending, In Progress, Completed)
- Update task status (start pending tasks, complete in-progress tasks)
- Edit task details (title, description, status)
- Delete tasks

## How It Works

1. **App (app.py)**: A Streamlit web interface that provides:
   - Task creation form in the sidebar
   - Task listing organized by status in tabs
   - Task management (edit, update status, delete)

2. **DynamoDB Utils (dynamodb_utils.py)**: Utility functions that interact with DynamoDB:
   - `put_item()`: Adds a new task item to the table
   - `get_all_items()`: Retrieves all tasks using scan operation
   - `get_item()`: Retrieves a specific task by task_id
   - `update_item()`: Updates task attributes (title, description, status)
   - `delete_item()`: Deletes a task from the table

## DynamoDB Features Used
- **PutItem**: Add new items to the table
- **Scan**: Retrieve all items from the table (for small datasets)
- **GetItem**: Retrieve a specific item by its primary key
- **UpdateItem**: Update item attributes using UpdateExpression
- **DeleteItem**: Remove items from the table

## Table Schema

The table uses the following schema:

- **Partition Key**: `task_id` (String) - Unique identifier for each task
- **Attributes**:
  - `title` (String) - Task title
  - `description` (String) - Task description
  - `status` (String) - Task status: "pending", "in_progress", or "completed"
  - `created_at` (String) - ISO timestamp of when the task was created

## Cleanup

To delete the table when done:

```bash
aws dynamodb delete-table \
  --table-name my-demo-tasks-22122025 \
  --region us-east-1
```

**Note:** Make sure to delete all items or empty the table before deleting it, though DynamoDB will delete the table regardless of its contents.

