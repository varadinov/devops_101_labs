#!/usr/bin/env python3
"""
SQS Worker - Polls messages from SQS queue and processes them.
Run this script in a separate terminal to process messages sent from the app.
"""

import time
import sys
from sqs_utils import get_queue_url, receive_messages, delete_message


def process_message(message_body: str, message_id: str):
    """
    Process a single message.
    
    Args:
        message_body: The content of the message
        message_id: The unique ID of the message
    """
    print(f"\n{'='*60}")
    print(f"📨 Processing Message ID: {message_id}")
    print(f"{'='*60}")
    print(f"Message Content: {message_body}")
    print(f"Processed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")


def main():
    """Main worker loop that continuously polls for messages."""
    # Get queue name from command line argument or use default
    if len(sys.argv) > 1:
        queue_name = sys.argv[1]
    else:
        queue_name = input("Enter SQS queue name (or set as command line argument): ").strip()
        if not queue_name:
            print("❌ Queue name is required!")
            sys.exit(1)
    
    # Get queue URL
    queue_url = get_queue_url(queue_name)
    if not queue_url:
        print(f"❌ Failed to get queue URL for '{queue_name}'. Make sure the queue exists.")
        sys.exit(1)
    
    print(f"🚀 Worker started. Polling queue: {queue_name}")
    print(f"📬 Queue URL: {queue_url}")
    print("⏳ Waiting for messages... (Press Ctrl+C to stop)\n")
    
    try:
        while True:
            # Receive messages with long polling (20 seconds)
            messages = receive_messages(queue_url, max_messages=10, wait_time_seconds=20)
            
            if messages:
                for message in messages:
                    message_body = message['Body']
                    message_id = message['MessageId']
                    receipt_handle = message['ReceiptHandle']
                    
                    # Process the message
                    process_message(message_body, message_id)
                    
                    # Delete the message from the queue after processing
                    if delete_message(queue_url, receipt_handle):
                        print(f"✅ Message {message_id} deleted from queue")
                    else:
                        print(f"⚠️ Warning: Failed to delete message {message_id}")
            else:
                # No messages received, print a heartbeat
                print(f"💓 No messages at {time.strftime('%Y-%m-%d %H:%M:%S')} - still polling...")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Worker stopped by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

