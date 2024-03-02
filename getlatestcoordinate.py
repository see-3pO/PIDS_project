from flask import jsonify
from connect import connect_db


latest_lat = None
latest_lng = None

def latest_coordinate():
    global latest_lat, latest_lng

    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        # Query to get the latest coordinates
        query = "SELECT latitude, longitude FROM current_coordinate ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(query)
        latest_coordinates = cursor.fetchone()

        if latest_coordinates:
             # Convert to dictionary for JSON response
            latest_lat = latest_coordinates['latitude']
            latest_lng = latest_coordinates['longitude']
            print("Updated coordinates:", latest_lat, latest_lng)
            return  latest_lat, latest_lng
        else:
            print("No coordinates found")
            return None, None
        
    except Exception as e:
         print("Error:", str(e))
         return None, None

    finally:
        # Close MySQL connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()