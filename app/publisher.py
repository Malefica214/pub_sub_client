import paho.mqtt.publish as publish
from pydantic import BaseModel
import json, os, logger

log = logger.setup_logger()

HOST_NAME = os.environ.get('HOST_NAME') or "127.0.0.1"
USERNAME = os.environ.get('USERNAME') or "francesca"
PASSWORD = os.environ.get('PASSWORD') or "francesca"

class Message(BaseModel):
    addresses_id: str
    request:str
    sender_id: str
    payload: str 
    
"""
    in questa zona bisognerebbe
    1. reperire le informazioni dei due utenti, (forse le manderà direttamente il front)
    2. montare il messaggio dipendentemente dal tipo di richiesta
"""

def send_request(addresses_id: str, request:str, sender_id: str, payload: str):
    log.debug(f"Send request {json.dumps(payload)}")
    publish.single(f"{addresses_id}/{request}/{sender_id}", payload=json.dumps(payload), qos=1, retain=True, 
                client_id=f"client-{sender_id}",
                hostname=HOST_NAME, auth={"username": USERNAME, "password": PASSWORD})