from fastapi import FastAPI, Security, WebSocket, WebSocketDisconnect
import toml, logger, asyncio, os
import paho.mqtt.client as mqtt

log = logger.setup_logger()

def get_app_config():
    config = toml.load("./pyproject.toml")
    return config["tool"]["bean_message"]

def get_app_message():
    messages = toml.load("./pyproject.toml")
    return messages["message"]["it"]

app_config = get_app_config()
app_messages = get_app_message()

app = FastAPI(
    title=app_config["title"],
    description=app_config.get("description"),
    version= app_config.get("version")
)

log.info(f"Start {app_config["title"]} - Subscriber")

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 9001  
USERNAME = os.environ.get('USERNAME') or "francesca"
PASSWORD = os.environ.get('PASSWORD') or "francesca"
TRANSPORT = os.environ.get('TRANSPORT') or "websockets"

connections = {}

def on_message(client, userdata, msg):
    log.info(f'Messagge received successfully {msg} - user_id {userdata}')
    user_id = userdata
    message_data = msg.payload.decode()
    if user_id in connections:
        log.info(f"Open connection for user {user_id}")
        websocket = connections[user_id]
        asyncio.run(websocket.send_json(message_data))

def on_connect(client, userdata, flags, reason_code, properties):
    log.info(f"""Connected with result code {reason_code}
             client : {client}
             user id : {userdata}
             properties: {properties}
             """)
    
@app.get('/', tags=["Subscriber"])
def health():
    return({
        "status": "UP"
    })
        
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    log.info(f"Open websocket channel")
    await websocket.accept()
    connections[user_id] = websocket
    log.info(f"Open connection {connections[user_id]}")
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, 
                        client_id=f"client-{user_id}", 
                        transport=TRANSPORT,
                        userdata=user_id)
    mqttc.username_pw_set(username=USERNAME, password=PASSWORD)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    topic = f"{user_id}/#"
    log.info(f"Subscribe to the topic {topic}")
    mqttc.subscribe(topic)
    mqttc.loop_start()
    
    try:
        while True:
            # Ricezione di eventuali messaggi WebSocket (es. comandi)
            log.info(f"Receiving text messages")
            await websocket.receive_text()
    except WebSocketDisconnect as ex:
        log.error(f"Websocket error {ex}")
        # Cleanup
        mqttc.loop_stop()
        mqttc.disconnect()
        del connections[user_id]