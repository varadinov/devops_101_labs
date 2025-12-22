import boto3
from botocore.exceptions import ClientError
from typing import Optional, List, Dict


def get_sqs_client():
    """Initialize and return SQS client."""
    return boto3.client('sqs')


def send_message(queue_url: str, message_body: str) -> bool:
    """
    Send a message to an SQS queue.
    """
    try:
        sqs_client = get_sqs_client()
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print(f"Message sent successfully. MessageId: {response['MessageId']}")
        return True
    except ClientError as e:
        print(f"Error sending message: {e}")
        return False


def receive_messages(queue_url: str, max_messages: int = 1, wait_time_seconds: int = 20) -> List[Dict]:
    """
    Receive messages from an SQS queue.
    """
    try:
        sqs_client = get_sqs_client()
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=min(max_messages, 10),
            WaitTimeSeconds=wait_time_seconds
        )
        
        messages = response.get('Messages', [])
        return messages
    except ClientError as e:
        print(f"Error receiving messages: {e}")
        return []


def delete_message(queue_url: str, receipt_handle: str) -> bool:
    """
    Delete a message from an SQS queue after processing.
    """
    try:
        sqs_client = get_sqs_client()
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        return True
    except ClientError as e:
        print(f"Error deleting message: {e}")
        return False


def get_queue_url(queue_name: str) -> Optional[str]:
    """
    Get the URL of an SQS queue by name.
    """
    try:
        sqs_client = get_sqs_client()
        response = sqs_client.get_queue_url(QueueName=queue_name)
        return response['QueueUrl']
    except ClientError as e:
        print(f"Error getting queue URL: {e}")
        return None

