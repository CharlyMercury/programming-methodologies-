import paho.mqtt.client as mqtt


# Se llama a esta función cuando el cliente se quiere conectar al broker 
# También se hacen las suscripciones a tópicos
def on_connect(client, userdata, flags, reason_code, properties):
    topico_temperatura = "test/topic"
    print(f"Successfully Connected with result code {reason_code}")
    client.subscribe(topico_temperatura, qos=1)
    print(f"Me suscribí al tópico {topico_temperatura}")


# Se llama esta función cuando llega un mensaje a la suscripción
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # if msg.topic == "temperatura1":
    #     client.publish("temperatura2", "Recibí mensaje")
    

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set("foco_sala", "Bob22esponja")
print("Conectando al broker...")

mqttc.tls_set() 

mqttc.connect("608359e51bfa42d5a47f3d14c8f5d47f.s1.eu.hivemq.cloud", 8883, 10)
mqttc.loop_forever()
