import asyncio
import websockets
import json

async def test_websocket_notifications(user_id:str):
    # URL del tuo endpoint WebSocket
    uri = f"ws://127.0.0.1:8000/ws/{user_id}"

    async with websockets.connect(uri) as websocket:
        print("Connesso al WebSocket")
        try:
            while True:
                # Ricevi notifiche dal server
                message = await websocket.recv()
                print("Notifica ricevuta:", json.dumps(message))
        except websockets.ConnectionClosed as ex:
            print(ex)
            print("Connessione chiusa dal server")
        except Exception as e:
            print("Errore:", e)

# Esegui il test
asyncio.run(test_websocket_notifications("f001"))
