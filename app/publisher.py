import paho.mqtt.publish as publish
from pydantic import BaseModel
import json

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
    print(json.dumps(payload))
    publish.single(f"{addresses_id}/{request}/{sender_id}", payload=json.dumps(payload), qos=1, retain=True, 
                client_id="diet-match-moble-dev",
                hostname="127.0.0.1", auth={"username": "francesca", "password": "francesca"})