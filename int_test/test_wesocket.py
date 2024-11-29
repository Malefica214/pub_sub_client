import asyncio, websockets, json, os

"""
    A simple script for listen websocket end point
"""
HOST_NAME = os.environ.get('HOST_NAME') or "127.0.0.1"
PORT = '9100'

async def test_websocket_notifications(user_id:str):
    uri = f"ws://{HOST_NAME}:{PORT}/ws/{user_id}"

    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")
        try:
            while True:
                message = await websocket.recv()
                print("Notification received:", json.dumps(message))
        except websockets.ConnectionClosed as ex:
            print(ex)
            print("Connection closed by server")
        except Exception as e:
            print("Error:", e)

# Run test
asyncio.run(test_websocket_notifications("francesca"))
