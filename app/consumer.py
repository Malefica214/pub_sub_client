import pika
import json

"""
    CONSUMER
"""

RABBITMQ_HOST='localhost'
QUEUE_NAME = "message"
PROCESSED_QUEUE_NAME= f"processed_{QUEUE_NAME}"

def callback(ch, method, properties, body):
    """Elaborazione del messaggio ricevuto."""
    message = json.loads(body)
    print(f"Notifica ricevuta: {message}")
    # Simula l'elaborazione (esempio: invio tramite email/SMS)
    #dead_letter_queue(message)
    # Conferma del messaggio come elaborato
    #ch.basic_ack(delivery_tag=method.delivery_tag)
    
    
def dead_letter_queue(message_data: dict):
    """Esegui un'azione con la notifica (esempio: invio email)."""
    print(f"Invio notifica a {message_data['addressee_id']}: {message_data['message']}")
    dlq_connetion = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, 
                                    credentials=pika.PlainCredentials('francesca', 'francesca')))
    dlq_channel = dlq_connetion.channel()

    dlq_channel.queue_declare(queue=PROCESSED_QUEUE_NAME, durable=True)
    dlq_channel.basic_publish(
        exchange='',
        routing_key=PROCESSED_QUEUE_NAME,
        body=json.dumps(message_data),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    #dlq_connetion.close()
    
    """
    configurazione dei messaggi:
    
    exchange=message.type,
    routing_key=message.addressee_id,
    """
def start_consumer(addressee_id: str, message_type: str):
    """Avvia il consumatore."""
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, 
                        credentials=pika.PlainCredentials('francesca', 'francesca')))    

    channel = connection.channel()

    channel.exchange_declare(exchange=message_type, exchange_type='direct', durable=True)

    result = channel.queue_declare(queue=addressee_id, exclusive=False, durable=True)
    queue_name = result.method.queue
    # Dichiarazione della coda
    #channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(exchange=message_type, queue=queue_name, routing_key=addressee_id)
    
    # Registrazione della funzione callback
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print("Consumatore in ascolto...")
    channel.start_consuming()
     
start_consumer(addressee_id='pina', message_type='love')



