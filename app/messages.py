from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal
import pika
import uuid
import json

class Message(BaseModel):
     addressee_id: str
     sender_id: str
     type: str 
     message: str
     state: Literal['PENDING', 'REJECT', 'ACCEPT']
     created_at: datetime | str
     
RABBITMQ_HOST='localhost'
QUEUE_NAME = "message"

def publish_message(message: Message):
     """Pubblica un messaggio in Rabbit"""
     try:
          message_data = message.model_dump()
          connetion = pika.BlockingConnection(
               pika.ConnectionParameters(host=RABBITMQ_HOST, 
                                         credentials=pika.PlainCredentials('francesca', 'francesca')))
          channel = connetion.channel()
          
          message_data['id'] = str(uuid.uuid4().hex)

          channel.queue_declare(queue=QUEUE_NAME, durable=True)
          channel.exchange_declare(exchange=message.type, exchange_type='direct', durable=True)
          
          channel.basic_publish(
               exchange=message.type,
               routing_key=message.addressee_id,
               body=json.dumps(message_data),
               properties=pika.BasicProperties(delivery_mode=2)
          )
          
          connetion.close()
     
     except Exception as e:
          raise HTTPException(status_code=500, detail=f"Errore nell'invio del messaggio: {str(e)}")


