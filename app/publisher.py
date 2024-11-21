import paho.mqtt.publish as publish

publish.single("first_topic/inbox/pluto", payload="Hello, world!", qos=1, retain=True, 
               client_id="pyclient-pub",
               hostname="127.0.0.1", auth={"username": "francesca", "password": "francesca"})

publish.single("first_topic/inbox/pippo", payload="Hello, world!2", qos=1, retain=True, 
               client_id="pyclient-pub2",
               hostname="127.0.0.1", auth={"username": "francesca", "password": "francesca"})
