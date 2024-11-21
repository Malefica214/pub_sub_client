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
DLQ_PREFIX = 'dlq_'
EXCHANGE_NAME = 'generic_exchange'

def publish_message(message_input: Message):
    """Pubblica un messaggio in RabbitMQ"""
    try:
        message = message_input.model_dump()
        # Aggiungi un identificativo univoco al messaggio
        message['id'] = str(uuid.uuid4().hex)

        # Connessione a RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                credentials=pika.PlainCredentials('francesca', 'francesca')
            )
        )
        channel = connection.channel()

        # Dichiarazione dell'exchange generico (direct exchange)
        # exchange = message type
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct', durable=True)

        # Dichiarazione della coda generica (tutti i messaggi arriveranno qui)
        channel.queue_declare(queue=QUEUE_NAME, durable=True, arguments={
            'x-dead-letter-exchange': '',  
            'x-dead-letter-routing-key': message_input.addressee_id
        })

        # Pubblicazione del messaggio nell'exchange
        routing_key = message.get('addressee_id', 'default_routing_key')
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,  # Routing key basato sul destinatario
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  # Persistenza del messaggio
            )
        )

        connection.close()
    except Exception as e:
        print(f"Errore nell'invio del messaggio: {e}")