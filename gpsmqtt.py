from flask import Flask, current_app as app
from flask_mqtt import Mqtt
import json
from threading import Event
from flask_socketio import SocketIO, emit
from winlocation import getLoc

app = Flask(__name__)
mqtt = Mqtt()
socketio = SocketIO(app, cors_allowed_origins="*")
coordinates =[]
# coordinates_event = Event()

def getting_json_mqtt():
    global coordinates

    with app.app_context():
        app.config['MQTT_BROKER_URL'] = '192.168.209.82'
        app.config['MQTT_BROKER_PORT'] = 1883
        app.config['MQTT_KEEPALIVE'] = 5
        app.config['MQTT_TLS_ENABLED'] = False

        @mqtt.on_connect()
        def handle_connect(client, userdata, flags, rc):
            if rc == 0:
                print('Connected to MQTT successfully')
                mqtt.subscribe('/gpscoordinates/testpub')
            else:
                print('Bad connection. Code:', rc)

        @mqtt.on_message()
        def handle_mqtt_message(client, userdata, message):
            print(message)
            coordinates.append(message.payload)
            print(f"Received message: {message.payload}")
            # coordinates_event.set()
            socketio.emit('mqttdata', {'coordinates': coordinates[0]}, namespace='/test')
        #     try:
        #         json_data = json.loads(message_payload)
        #         coordinates[0] = json_data['latitude']
        #         coordinates[1] = json_data['longitude']

        #         print(f"Latitude: {coordinates[0]}, Longitude: {coordinates[1]}")
        #     except Exception as e:
        #         print(f"Error: {e}")

        # return coordinates[0], coordinates[1]
def get_current_coordinates():
    # coordinates_event.wait()
    if coordinates:
        latitude_pos = coordinates[0][0]
        longitude_pos = coordinates[0][1]
        print(coordinates[0])
        return latitude_pos, longitude_pos
    else:
        print("No coordinates received yet.")
        return getLoc()