# S3 Demo

This demo shows how to use Amazon Simple Storage Service (S3) to upload, list, preview, and delete images.

## Setup

### 1. Create S3 Bucket

First, create an S3 bucket using the AWS CLI:

```bash
export AWS_PROFILE=demo
aws s3api create-bucket \
  --bucket my-demo-bucket-22122025 \
  --region us-east-1
```

The command will create a new S3 bucket. Note the bucket name for the next step.

**List buckets (if needed):**

```bash
aws s3 ls --region us-east-1
```

### 2. Configure Streamlit Secrets

Create the secrets file for the Streamlit app:

```bash
mkdir -p .streamlit
echo 'bucket_name = "my-demo-bucket-22122025"' > .streamlit/secrets.toml
```

### 3. Run the Application

Start the Streamlit app:

```bash
cd 01_s3
uv run streamlit run app.py
```

The app will open in your browser. You can:
- Upload images from your local machine to S3
- View all images stored in the bucket
- Preview images directly in the browser
- Delete images from the bucket

## How It Works

1. **App (app.py)**: A Streamlit web interface that provides:
   - Image upload functionality (supports JPG, JPEG, PNG, GIF, BMP, WEBP)
   - Image listing with thumbnails
   - Image preview
   - Image deletion

2. **S3 Utils (s3_utils.py)**: Utility functions that interact with S3:
   - `upload_image()`: Uploads image files to S3 with proper content types
   - `list_images()`: Lists all image files in the bucket
   - `preview_image()`: Downloads images from S3 for preview
   - `delete_image()`: Deletes images from S3

## S3 Features Used

- **PutObject**: Upload files to S3 with metadata (ContentType)
- **ListObjectsV2**: List all objects in the bucket with filtering
- **GetObject**: Download objects from S3 for preview
- **DeleteObject**: Remove objects from S3

## Cleanup

To delete the bucket when done (note: bucket must be empty first):

```bash
# Delete all objects in the bucket
aws s3 rm s3://my-demo-bucket-22122025 --recursive

# Delete the bucket
aws s3api delete-bucket \
  --bucket my-demo-bucket-22122025 \
  --region us-east-1
```