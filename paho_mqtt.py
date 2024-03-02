from flask import current_app as app
import random
from paho.mqtt import client as mqtt_client
import json, time
from winlocation import getLoc

broker = '192.168.0.105'
port = 1883
topic = '/gpscoordinates/testpub'
client_id = f'subscribe-{random.randint(0, 100)}'
lat = None
lng = None
# coordinates = []
def connect_mqtt()-> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
        else:
            print("Failed to connect, return code %d\n",rc)
    
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    global lat, lng
    def on_message(client, userdata, message):
        print(f"Received message: {message.payload}")
        # coordinates.append(message.payload)
        try:
            payload_str = message.payload.decode('utf-8')
            json_data = json.loads(payload_str)
            lat = json_data.get('latitude')
            print(lat)
            lng = json_data.get('longitude')
            print(lng)
            # coordinates.append((json_data.get('latitude'), json_data.get('longitude')))
        except Exception as e:
            print(e)
       
    
    client.subscribe(topic)
    client.on_message = on_message

def get_current_coordinates():
    global lat, lng
    if lat is not None and lng is not None:
        latitude_pos = lat
        longitude_pos = lng
        # print(coordinates[0])
        return latitude_pos, longitude_pos
    else:
        print("No coordinates received yet.")
        return None, None

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()  # Start the loop in the background
    time.sleep(5)  # Give some time for messages to be received
    get_current_coordinates()
    print("Continuing execution...") 
    # client.loop_forever()

if __name__ == '__main__':
    run()