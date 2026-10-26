import asyncio
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mounting the static folder to serve HTML and JS
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accepting the WebSocket connection
    try:
        while True:
            # Sending current datetime every 30 seconds
            print("Sending current server time")
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await websocket.send_text(f"Current server time: {now}")
            await asyncio.sleep(10)  # Wait for 30 seconds
    except WebSocketDisconnect:
        print("Client disconnected")