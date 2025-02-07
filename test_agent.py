import asyncio
import websockets
import json
from datetime import datetime

async def test_agent():
    uri = "ws://localhost:8000/chat"
    
    # Example test message for scheduling a meeting
    test_message = {
        "content": "Schedule a meeting with the client.",
        "category": "schedule",
        "metadata": {
            "title": "Client Meeting",
            "start_time": "2025-02-10T10:00:00",  # Use ISO 8601 format
            "end_time": "2025-02-10T11:00:00",    # Use ISO 8601 format
            "email": "client@example.com"
        }
    }
    
    async with websockets.connect(uri) as websocket:
        # Send the test message
        await websocket.send(json.dumps(test_message))
        
        # Wait for a response from the WebSocket server
        response = await websocket.recv()
        response_data = json.loads(response)
        
        # Print the server's response safely
        timestamp = response_data.get('timestamp', 'N/A')  # Use 'N/A' if timestamp is missing
        category = response_data.get('category', 'N/A')
        server_response = response_data.get('response', 'No response')

        print(f"Server Response at {timestamp}:")
        print(f"Category: {category}")
        print(f"Response: {server_response}")

# Run the test
asyncio.get_event_loop().run_until_complete(test_agent())
