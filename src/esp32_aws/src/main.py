"""

{"state":{"led":{"onboard":1}}}

"""
import os
import time
import ujson
import dht
from machine import Pin
import network
from simple import MQTTClient
import mh_z19


#Enter your wifi SSID and password below.
# wifi_ssid = "IZZI-B10C-5G"
# wifi_password = "hHqKtA2cGf232RJJYA"
wifi_ssid = "CNAD_2025_5G"
wifi_password = "CNAD2025$$"

#Enter your AWS IoT endpoint. You can find it in the Settings page of
#your AWS IoT Core console. 
aws_endpoint = b'a21xc2x2m4yaib-ats.iot.us-east-1.amazonaws.com'

#If you followed the blog, these names are already set.
thing_name = "Prueba_embeeded_systems"
client_id = "Prueba_embeeded_systems"
private_key = "private.key"
device_cert = "device_cert.crt"
cacert_cert = "root.pem"

#Read the files used to authenticate to AWS IoT Core
with open(private_key, 'rb') as f:
    key = f.read()
with open(device_cert, 'rb') as f:
    cert = f.read()
with open(cacert_cert, 'rb') as f:
    cacert = f.read()
    
#These are the topics we will subscribe to. We will publish updates to /update.
#We will subscribe to the /update/delta topic to look for changes in the device shadow.
topic_pub = "sensors"
topic_sub = "led"

#Define pins for LED and humidity-temperature sensor.
#The sensor and LED are built into the board, and no external connections are required.
dht_temp_hum = dht.DHT11(Pin(4))
led = Pin(2, Pin.OUT)
info = os.uname()

# CO2 Sensor
mhz = mh_z19.MHZ19(17, 16)
# detection range 0-5000PPM
mhz.set_detection_range(5000)
# read co2 once
co2 = mhz.read_co2()
# read co2 continuously every 5 secs
mhz.read_co2_continuous(5000)


#Connect to the wireless network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to network...')
    print("Charly...")
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
        print("Charly...")
        pass

    print('Connection successful')
    print('Network config:', wlan.ifconfig())

def mqtt_connect(client=client_id, endpoint=aws_endpoint):
    mqtt = MQTTClient(
        client_id=client, 
        server=endpoint, 
        port=8883, 
        keepalive=1200, ssl=True, ssl_params={'key':key, 'cert':cert, 'cadata': cacert, 'server_side':False})
    print("Connecting to AWS IoT...")
    mqtt.connect()
    print("Done")
    return mqtt

def mqtt_publish(client, topic=topic_pub, message=''):
    print("\n \t Publishing message...")
    client.publish(topic, message)
    print(message)

def mqtt_subscribe(topic, msg):
    print("Message received...")
    message = ujson.loads(msg)
    print(topic, message)
    if message['state']['led']:
        led_state(message)
    print("Done")

def led_state(message):
    print(message['state']['led']['onboard'])
    led.value(message['state']['led']['onboard'])

# {"state":{"led":{"onboard":1}}}

#We use our helper function to connect to AWS IoT Core.
#The callback function mqtt_subscribe is what will be called if we 
#get a new message on topic_sub.
try:
    mqtt = mqtt_connect()
    mqtt.set_callback(mqtt_subscribe)   
    mqtt.subscribe(topic_sub)
except Exception as err:
    print("Unable to connect to AWS.", err)


while True:
#Check for messages.
    try:
        mqtt.check_msg()
    except:
        print("Unable to check for messages.")
    
    dht_temp_hum.measure() 
    mhz.update()
    mesg = ujson.dumps({
        "state":{
            "reported": {
                "device": {
                    "client": client_id,
                    "uptime": time.ticks_ms(),
                    "hardware": info[0],
                    "firmware": info[2]
                },
                "sensors": {
                    "humidity": dht_temp_hum.humidity(),
                    "temperature": dht_temp_hum.temperature(),
                    "co2": mhz.get_co2()
                },
                "led": {
                    "onboard": led.value()
                }
            }
        }
    })

#Using the message above, the device shadow is updated.
    try:
        mqtt_publish(client=mqtt, message=mesg)
    except:
        print("Unable to publish message.")

#Wait for 10 seconds before checking for messages and publishing a new update.
    print("Sleep for 10 seconds")
    time.sleep(10)
