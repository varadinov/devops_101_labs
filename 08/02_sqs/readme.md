# SQS Demo

This demo shows how to use Amazon Simple Queue Service (SQS) to send and receive messages.

## Setup

### 1. Create SQS Queue

First, create an SQS queue using the AWS CLI:

```bash
export AWS_PROFILE=demo
aws sqs create-queue \
  --queue-name my-demo-queue-22122025 \
  --region us-east-1 \
  --attributes VisibilityTimeout=30,MessageRetentionPeriod=345600
```

The command will return a JSON response with the QueueUrl. Note the queue name for the next step.

**Get queue URL (if needed):**

```bash
aws sqs get-queue-url \
  --queue-name my-demo-queue-22122025 \
  --region us-east-1
```

### 2. Configure Streamlit Secrets

Create the secrets file for the Streamlit app:

```bash
mkdir -p .streamlit
echo 'queue_name = "my-demo-queue-22122025"' > .streamlit/secrets.toml
```

### 3. Run the Application

#### Start the Streamlit App (Message Sender)

In one terminal, start the Streamlit app:

```bash
cd 02_sqs
uv run streamlit run app.py
```

The app will open in your browser. You can enter messages and click "Send Message" to send them to the SQS queue.

#### Start the Worker (Message Processor)

In a separate terminal, start the worker to process messages:

```bash
cd 02_sqs
uv run python worker.py my-demo-queue-22122025
```

The worker will continuously poll the queue for messages and display them on the screen.

## How It Works

1. **App (app.py)**: A Streamlit web interface where you can enter messages and send them to the SQS queue
2. **Worker (worker.py)**: A background process that polls the queue, receives messages, processes them (displays on screen), and deletes them from the queue

## Queue Attributes Explained

- **VisibilityTimeout**: How long a message is hidden from other consumers after being received (30 seconds)
- **MessageRetentionPeriod**: How long messages stay in the queue if not processed (345600 seconds = 4 days)
- **ReceiveMessageWaitTimeSeconds**: Long polling wait time (20 seconds) - reduces API calls and costs

## Cleanup

To delete the queue when done:

```bash
# Get the QueueUrl and store it in a variable
QUEUE_URL=$(aws sqs get-queue-url --queue-name my-demo-queue-22122025 --region us-east-1 --query "QueueUrl" --output text)

# Now delete the queue using that variable
aws sqs delete-queue --queue-url "$QUEUE_URL"import boto3
```

