import paho.mqtt.client as mqtt

messages_list = []

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("francesca/#")

def on_message(client, userdata, msg):
    messages_list.append(f"{msg.topic}: {msg.payload.decode()} : {msg.qos}")
    print(messages_list)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='pyclient', transport="websockets")
mqttc.username_pw_set(username="francesca", password="francesca")
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("127.0.0.1", 9001, 60)
mqttc.loop_forever()