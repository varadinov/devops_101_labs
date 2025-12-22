import boto3
from botocore.exceptions import ClientError
from typing import List, Optional, Dict
from datetime import datetime
import uuid


def get_dynamodb_client():
    """Initialize and return DynamoDB client."""
    return boto3.client('dynamodb')


def get_dynamodb_resource():
    """Initialize and return DynamoDB resource."""
    return boto3.resource('dynamodb')


def table_exists(table_name: str) -> bool:
    """
    Check if a DynamoDB table exists.
    """
    try:
        dynamodb = get_dynamodb_client()
        response = dynamodb.describe_table(TableName=table_name)
        return response['Table']['TableStatus'] == 'ACTIVE'
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return False
        print(f"Error checking table: {e}")
        return False


def put_item(table_name: str, title: str, description: str = '', status: str = 'pending') -> Optional[str]:
    """
    Add a new task item to DynamoDB.
    """
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(table_name)
        
        task_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        
        table.put_item(
            Item={
                'task_id': task_id,
                'title': title,
                'description': description,
                'status': status,
                'created_at': created_at
            }
        )
        return task_id
    except ClientError as e:
        print(f"Error putting item: {e}")
        return None


def get_all_items(table_name: str) -> List[Dict]:
    """
    Get all items from a DynamoDB table using scan.
    """
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(table_name)
        
        response = table.scan()
        items = response.get('Items', [])
        
        # Handle pagination if there are more items
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))
        
        # Sort by created_at (newest first)
        items.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return items
    except ClientError as e:
        print(f"Error scanning items: {e}")
        return []


def get_item(table_name: str, task_id: str) -> Optional[Dict]:
    """
    Get a specific item from DynamoDB by task_id.
    """
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(table_name)
        
        response = table.get_item(
            Key={
                'task_id': task_id
            }
        )
        
        return response.get('Item')
    except ClientError as e:
        print(f"Error getting item: {e}")
        return None


def update_item(table_name: str, task_id: str, title: str = None, description: str = None, status: str = None) -> bool:
    """
    Update an item in DynamoDB.
    """
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(table_name)
        
        update_expression_parts = []
        expression_attribute_values = {}
        expression_attribute_names = {}
        
        if title is not None:
            update_expression_parts.append("#title = :title")
            expression_attribute_values[':title'] = title
            expression_attribute_names['#title'] = 'title'
        
        if description is not None:
            update_expression_parts.append("#description = :description")
            expression_attribute_values[':description'] = description
            expression_attribute_names['#description'] = 'description'
        
        if status is not None:
            update_expression_parts.append("#status = :status")
            expression_attribute_values[':status'] = status
            expression_attribute_names['#status'] = 'status'
        
        if not update_expression_parts:
            return False
        
        update_expression = "SET " + ", ".join(update_expression_parts)
        
        update_kwargs = {
            'Key': {'task_id': task_id},
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': expression_attribute_values,
            'ReturnValues': 'UPDATED_NEW'
        }
        
        if expression_attribute_names:
            update_kwargs['ExpressionAttributeNames'] = expression_attribute_names
        
        table.update_item(**update_kwargs)
        return True
    except ClientError as e:
        print(f"Error updating item: {e}")
        return False


def delete_item(table_name: str, task_id: str) -> bool:
    """
    Delete an item from DynamoDB.
    """
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(table_name)
        
        table.delete_item(
            Key={
                'task_id': task_id
            }
        )
        return True
    except ClientError as e:
        print(f"Error deleting item: {e}")
        return False

