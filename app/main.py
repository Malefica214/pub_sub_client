from fastapi import FastAPI, Security
import toml
import asyncio
from fastapi import WebSocket
from notification import insert_new_notification, get_notifiche, update_state, watch_notifications

def get_app_config():
    config = toml.load("./pyproject.toml")
    return config["tool"]["bean_notification"]

app_config = get_app_config()

app = FastAPI(
    title=app_config["title"],
    description=app_config.get("description"),
    version= app_config.get("version")
)

@app.get('/')
def health():
    return({
        "status": "UP"
    })

@app.websocket("/ws/{addressee_id}")
async def websocket_notifiche(websocket: WebSocket, addressee_id: str):
    await websocket.accept()
    try:
        async for change in watch_notifications(addressee_id=addressee_id):
            new_notification = change["fullDocument"]
            await websocket.send_json({'id': str(new_notification["_id"]),
                'addressee_id': new_notification["addressee_id"],
                'sender_id': new_notification["sender_id"],
                'type': new_notification.get("type"),
                'message': new_notification["message"],
                'state': new_notification["state"],
                'created_at': new_notification["created_at"]})
    except Exception as e:
        print(f"Errore WebSocket: {e}")
    finally:
        await websocket.close()