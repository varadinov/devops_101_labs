import boto3
from botocore.exceptions import ClientError
from typing import List, Optional
import io


def get_s3_client():
    """Initialize and return S3 client."""
    return boto3.client('s3')


def upload_image(bucket_name: str, file_name: str, file_data: bytes, content_type: str = 'image/jpeg') -> bool:
    """
    Upload an image to S3.
    """
    try:
        s3_client = get_s3_client()
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_data,
            ContentType=content_type
        )
        return True
    except ClientError as e:
        print(f"Error uploading file: {e}")
        return False


def list_images(bucket_name: str, prefix: str = '') -> List[dict]:
    """
    List all images in the S3 bucket.
    """
    try:
        s3_client = get_s3_client()
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        
        if 'Contents' not in response:
            return []
        
        # Filter for common image extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        images = []
        for obj in response['Contents']:
            key = obj['Key']
            if any(key.lower().endswith(ext) for ext in image_extensions):
                images.append({
                    'Key': key,
                    'LastModified': obj['LastModified']
                })
        
        return images
    except ClientError as e:
        print(f"Error listing images: {e}")
        return []


def delete_image(bucket_name: str, file_name: str) -> bool:
    """
    Delete an image from S3.
    """
    try:
        s3_client = get_s3_client()
        s3_client.delete_object(Bucket=bucket_name, Key=file_name)
        return True
    except ClientError as e:
        print(f"Error deleting file: {e}")
        return False


def preview_image(bucket_name: str, file_name: str) -> Optional[bytes]:
    """
    Download an image from S3 for preview.
    """
    try:
        s3_client = get_s3_client()
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        return response['Body'].read()
    except ClientError as e:
        print(f"Error downloading file: {e}")
        return None

