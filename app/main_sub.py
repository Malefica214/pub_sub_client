from fastapi import FastAPI, Security, WebSocket, WebSocketDisconnect
import toml
import paho.mqtt.client as mqtt
import asyncio
import json

def get_app_config():
    config = toml.load("./pyproject.toml")
    return config["tool"]["bean_message"]

app_config = get_app_config()

app = FastAPI(
    title=app_config["title"],
    description=app_config.get("description"),
    version= app_config.get("version")
)

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 9001  

connections = {}

def on_message(client, userdata, msg):
    print('messaggio ricevuto ')
    user_id = userdata
    message_data = msg.payload.decode()
    if user_id in connections:
        websocket = connections[user_id]
        asyncio.run(websocket.send_json(message_data))

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
        
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    print("connesso allo websocket di fastapi")
    await websocket.accept()
    connections[user_id] = websocket
    
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, 
                        client_id=f"client-{user_id}", 
                        transport="websockets",
                        userdata=user_id)
    mqttc.username_pw_set(username="francesca", password="francesca")
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    topic = f"{user_id}/#"
    mqttc.subscribe(topic)
    mqttc.loop_start()
    
    try:
        while True:
            # Ricezione di eventuali messaggi WebSocket (es. comandi)
            await websocket.receive_text()
    except WebSocketDisconnect as ex:
        print(ex)
        # Cleanup
        mqttc.loop_stop()
        mqttc.disconnect()
        del connections[user_id]