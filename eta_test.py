from connect import connect_db
from test_input import test_input
from gpsmqtt import get_current_coordinates
from winlocation import getCoords, getLoc
import mysql.connector
import googlemaps
import requests
import json
from getlatestcoordinate import latest_coordinate
from config import DISTANCEMATRIX_API_KEY


def eta():
    destination_lat = None
    destination_lng = None

    origin_lat = None  
    origin_lng = None  
      
    stoplist = []

    try:
        conn = connect_db()
        cursor = conn.cursor()
        # query to fetch data from the database
        query = """ 
            SELECT 
                bus_stop.stop_id, bus_stop.stop_name, bus_stop.latitude, bus_stop.longitude,
                route_stops.route_id, route_stops.stop_id, route_stops.stop_order
            FROM bus_stop 
            INNER JOIN route_stops ON bus_stop.stop_id = route_stops.stop_id 
            INNER JOIN bus_route ON route_stops.route_id = bus_route.route_id
            WHERE bus_route.route_name='Alpha to Foxtrot'
            """
        cursor.execute(query)
        results = cursor.fetchall()
        stop_id_list = list(map(lambda x: x[0], results))
        stop_name_list = list(map(lambda x: x[1], results))
        latitude_list = list(map(lambda x: x[2], results))
        better_latitude_list = [float(a) for a in latitude_list]
        longitude_list = list(map(lambda x: x[3], results))
        better_longitude_list = [float(a) for a in longitude_list]
        

        test_lat, test_lng = latest_coordinate()
        print(test_lat)
        print(test_lng)
        

        if test_lat in better_latitude_list and test_lng in better_longitude_list:
             print("Test coordinates present in the list.")
             for i in range(len(better_latitude_list) - 1):
                if (test_lat, test_lng) == (better_latitude_list[i], better_longitude_list[i]):
                    origin_lat = better_latitude_list[i]
                    origin_lng = better_longitude_list[i]

                    destination_lat = better_latitude_list[i + 1]
                    destination_lng = better_longitude_list[i + 1]

                    next_stop_name = stop_name_list[i + 1]
                    

                    stoplist.append(stop_id_list[i])
                    print(stoplist)
        else:
            combined_list = list(zip(better_latitude_list, better_longitude_list,stop_name_list))
            print(combined_list)

            if test_lat is not None and test_lng is not None:
                found = False
                for i in range(len(combined_list)):
                    if test_lat < combined_list[i][0]:
                        print(f"Next destination coordinates: ({combined_list[i][0]}, {combined_list[i][1]})")
                        origin_lat = test_lat
                        origin_lng = test_lng

                        destination_lat = combined_list[i][0]
                        destination_lng = combined_list[i][1]

                        next_stop_name = combined_list[i][2]

                        found = True
                        break

                if not found:
                    print("No destination with greater latitude found.")
            else:
                print("Invalid test coordinates: test_lat or test_lng is None.")

         
        
        if (origin_lat is not None and origin_lng is not None and destination_lat is not None and destination_lng is not None):
                origin = (origin_lat, origin_lng)
                destination = (destination_lat, destination_lng)
                mode = "walking"
                # traffic_model="best_guess"

                gmaps = googlemaps.Client(key=DISTANCEMATRIX_API_KEY)
                try:
                    my_dist = gmaps.distance_matrix(origin, destination, mode=mode)['rows'][0]['elements'][0] 
                    dist_string = json.dumps(my_dist)
                    dist_data = json.loads(dist_string)
                    print(dist_data)
                    duration_text = dist_data['duration']['text']
                    
                    return duration_text, next_stop_name
                except googlemaps.exceptions.HTTPError as e:
                    print("HTTP Error:", e)
    
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()
