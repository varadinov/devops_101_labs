import streamlit as st
from sqs_utils import send_message, get_queue_url

st.set_page_config(page_title="SQS Message Sender", layout="wide")

st.title("📨 SQS Message Sender")

# Load queue name from Streamlit secrets
try:
    queue_name = st.secrets["queue_name"]
    if not queue_name or queue_name == "your-queue-name-here":
        st.error("⚠️ Please configure the queue name in .streamlit/secrets.toml")
        st.stop()
except KeyError:
    st.error("⚠️ 'queue_name' not found in .streamlit/secrets.toml. Please add it.")
    st.stop()

# Get queue URL
queue_url = get_queue_url(queue_name)
if not queue_url:
    st.error(f"❌ Failed to get queue URL for '{queue_name}'. Make sure the queue exists.")
    st.stop()

st.info(f"📬 Connected to queue: **{queue_name}**")

# Main input area
st.header("Send Message")

message_input = st.text_input(
    "Enter your message:",
    placeholder="Type your message here...",
    key="message_input"
)

if st.button("📤 Send Message", type="primary"):
    if message_input:
        if send_message(queue_url, message_input):
            st.success(f"✅ Message sent successfully: '{message_input}'")
            # Clear the input field
            st.rerun()
        else:
            st.error("❌ Failed to send message. Check your AWS credentials and queue configuration.")
    else:
        st.warning("⚠️ Please enter a message before sending.")

st.divider()

st.markdown("""
### How it works:
1. Enter a message in the input field above
2. Click the "Send Message" button
3. The message will be sent to the SQS queue
4. Run the worker script (`worker.py`) in a separate terminal to process messages
""")

