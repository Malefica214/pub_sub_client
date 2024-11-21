import pika


queue_name = 'queue_prova'
rabbitmq_host = 'localhost'  # Assicurati che questo sia l'host corretto di RabbitMQ

def callback(ch, method, properties, body, reply_to_filter):
    if properties.reply_to == reply_to_filter:
        print(f"Properties: {properties}")
        print(f"Headers: {properties.headers}")
        print(f"Messaggio filtrato: {body.decode()}")
    else:
        print("Messaggio non filtrato")

# Funzione per avviare il consumer in un thread separato
def start_consumer(reply_to_filter: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', 
                                                                credentials=pika.PlainCredentials('francesca', 'francesca')))  
    channel = connection.channel()

    # Consumatore parametrizzato
    def on_message(ch, method, properties, body):
        callback(ch, method, properties, body, reply_to_filter)

    channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)
    print("In attesa di messaggi...")
    channel.start_consuming()