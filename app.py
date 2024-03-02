
from flask import Flask, render_template,url_for,redirect,session,jsonify
from display_fare import display_fare
from travel_time import get_local_ip_address
from register import registration
from login import login_user
from logout import logging_out
from eta_test import eta
import geocoder
from threading import Thread
from gpsmqtt import getting_json_mqtt, get_current_coordinates, socketio
# from gpsmqtt import getting_json_mqtt
from flask_mqtt import Mqtt
import json
import time
from winlocation import getCoords, getLoc
# import eventlet
# from flask_socketio import SocketIO
# from testapistatus import get_distance_matrix

app = Flask(__name__, instance_relative_config=True)
# socketio.init_app(app)


#load configuration from the instance folder
app.config.from_pyfile('config.py')

# Start the MQTT thread
# mqtt_thread = Thread(target=getting_json_mqtt)
# mqtt_thread.start()

@app.route('/tts')
def test_speech():
    return render_template('test.html')
# @app.route('/test')
# def test_api():
#     return get_distance_matrix()

@app.route('/get_latest_data', methods=['GET'])
def get_latest_data():
    duration_text, next_stop_name = eta()
    return jsonify({'duration': duration_text, 'next_stop': next_stop_name})


@app.route('/testcurrentloc')
def test_pclocation():
    pos_lat, pos_lng = getLoc()
    return render_template('map.html',pos_lat=pos_lat, pos_lng=pos_lng)

@app.route('/getgps')
def get_gps():
    lat, long = get_current_coordinates()
    return render_template('map.html',latitude = lat, longitude = long)

@app.route('/display')
def display_page():
  return display_fare()

@app.route('/')
def homePage():
    return login_user()

@app.route('/hichiri')
def test_eta():
    duration_text, next_stop_name = eta()
    return render_template('map.html',duration=duration_text, next_stop_name=next_stop_name)
 

# register page
@app.route('/register/', methods=['GET', 'POST'])
def register():
    
    return registration()
    

# login page
@app.route('/login/', methods=['GET', 'POST'])
def login():
   return login_user()

@app.route('/login/logout')
def logout():
    return logging_out()


@app.route('/login/home')
def home():
    if 'loggedin' in session:
        return render_template('main.html', username=session['username'])
    return redirect(url_for('login'))

        
if __name__ == '__main__':
    # getting_mqttdata()
    app.run(host='0.0.0.0', port=5000, debug=True)
    # socketio.run(app, debug=True)


     

