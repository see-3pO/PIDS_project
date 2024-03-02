from connect import connect_db
import googlemaps
import mysql.connector
import socket
import requests,json
from config import DISTANCEMATRIX_API_KEY

#display travel time 
def map_page():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        coordinates_query = 'SELECT stop_name, latitude, longitude FROM bus_stop'
        cursor.execute(coordinates_query)
         # Initialize an empty list to store the rows
        results = []
        for row in cursor.fetchall():
            stop_data = {
                'stop_name': row[0],
                'latitude': row[1],
                'longitude': row[2]
            }
            # Append each row to the results list
            results.append(stop_data)
        for result in results:
            latitude_coordinate = result['latitude']
            longitude_coordinate= result['longitude']
            name = result['stop_name']

            # print("Stop name:", name)
            if name == 'Alpha':
                origin_latitude = latitude_coordinate
                origin_longitude = longitude_coordinate
                # print(origin_latitude, origin_longitude)
            if name == 'Echo':
                dest_latitude = latitude_coordinate
                dest_longitude = longitude_coordinate
                # print(dest_latitude, dest_longitude)
        # Print 'yooh' only if neither 'Bravo' nor 'Echo' was found
        if origin_latitude is None and dest_latitude is None:
            print('yooh')

            # elif name == 'Foxtrot':
            
        if origin_latitude is not None and origin_longitude is not None and dest_latitude is not None and dest_longitude is not None:
            origin = (origin_latitude, origin_longitude)
            destination = (dest_latitude, dest_longitude)
            mode = "driving"
            # language = "en"
            # units = "metric" 
            # traffic_model = "best_guess"
            gmaps = googlemaps.Client(key=DISTANCEMATRIX_API_KEY)
            try:

                my_dist = gmaps.distance_matrix(origin, destination, mode=mode)['rows'][0]['elements'][0] 
                dist_string = json.dumps(my_dist)
                #creating a python dict called my dist_data from JSON
                dist_data = json.loads(dist_string)
                duration_text = dist_data['duration']['text']
                return duration_text
                # print(duration_text)
            except googlemaps.exceptions.HTTPError as e:
                print("HTTP Error:", e)

        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        return f"Error: {e}"
    finally:
        # Close the database connection
        if conn is not None:
            conn.close()
def get_local_ip_address():
    return socket.gethostbyname(socket.gethostname())