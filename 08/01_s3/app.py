import streamlit as st
from s3_utils import upload_image, list_images, delete_image, preview_image
import io

st.set_page_config(page_title="S3 Image Manager", layout="wide")

st.title("📸 S3 Image Manager")

# Load bucket name from Streamlit secrets
try:
    bucket_name = st.secrets["bucket_name"]
    if not bucket_name or bucket_name == "your-bucket-name-here":
        st.error("⚠️ Please configure the bucket name in .streamlit/secrets.toml")
        st.stop()
except KeyError:
    st.error("⚠️ 'bucket_name' not found in .streamlit/secrets.toml. Please add it.")
    st.stop()

# Sidebar for upload
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])
    
    if uploaded_file is not None:
        if st.button("Upload to S3"):
            file_data = uploaded_file.read()
            file_name = uploaded_file.name
            
            # Determine content type
            content_type = uploaded_file.type or 'image/jpeg'
            
            if upload_image(bucket_name, file_name, file_data, content_type):
                st.success(f"✅ Successfully uploaded {file_name}!")
                st.rerun()
            else:
                st.error(f"❌ Failed to upload {file_name}")

# Main area for listing and previewing
st.header("Images in S3")

if st.button("🔄 Refresh List"):
    st.rerun()

images = list_images(bucket_name)

if not images:
    st.info("No images found in the bucket.")
else:
    st.write(f"Found {len(images)} image(s)")
    
    # Display images in a grid
    cols = st.columns(3)
    
    for idx, image_info in enumerate(images):
        col = cols[idx % 3]
        
        with col:
            # Show thumbnail preview
            image_data = preview_image(bucket_name, image_info['Key'])
            if image_data:
                st.image(io.BytesIO(image_data), use_container_width=True, caption=image_info['Key'])
            else:
                st.error("Failed to load image")
            
            st.caption(f"Modified: {image_info['LastModified'].strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Delete button
            if st.button("🗑️ Delete", key=f"delete_{idx}"):
                if delete_image(bucket_name, image_info['Key']):
                    st.success(f"Deleted {image_info['Key']}")
                    st.rerun()
                else:
                    st.error(f"Failed to delete {image_info['Key']}")
            
            st.divider()

