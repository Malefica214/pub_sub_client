from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

class Notification(BaseModel):
     id : str
     addressee_id: str
     sender_id: str
     type: str | None
     message: str
     state: Literal['PENDING', 'REJECT', 'ACCEPT']
     created_at: datetime | str


uri = "mongodb+srv://francescabuso:A2dLjWy8whZ0WkVnYQpFDp2qph6wRT5DUJOYN@wasclient.iczkjnu.mongodb.net/?retryWrites=true&w=majority&appName=WasClient"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["bean-notifications"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

collection = db["notifications"]

def map_dict_to_notification(notification: dict):
    return Notification(id=str(notification["_id"]),
                      addressee_id=notification["addressee_id"],
                      sender_id=notification["sender_id"],
                      type=notification.get("type"),
                      message=notification["message"],
                      state=notification["state"],
                      created_at=notification["created_at"])

def insert_new_notification(addressee_id: str, sender_id: str, message: str, type: str):
        notification = {
            "addressee_id": addressee_id,
            "sender_id": sender_id,
            "message": message,
            "type": type,
            "state": 'PENDING', 
            "created_at": datetime.now().__format__("%Y-%m-%d %H:%M:%S %Z%z")
        }
        return collection.insert_one(notification)

def get_notifiche(addressee_id: str):
    notifications = collection.find({"addressee_id": addressee_id}).sort("created_at", -1)

    return [
            map_dict_to_notification(notification=notification)
            for notification in notifications
    ]
    
def update_state(notification_id: str, state : Literal['PENDING', 'REJECT', 'ACCEPT']):
    result = collection.update_one(
        {"_id": ObjectId(notification_id)},
        {"$set": {"state": state}}
    )
    if result.matched_count == 0:
        raise Exception(status_code=404, detail="Notification not found")
    return result



#insert_new_notification(addressee_id='pippo', sender_id='pluto', message='hola amico', type='richiesta_collegamento')
notifiche = get_notifiche(addressee_id='pippo')
#notifica = update_state(notification_id='673c99b01961eb0aceee91c8', state='ACCEPT')
print(notifiche)

#collection.delete_many({})