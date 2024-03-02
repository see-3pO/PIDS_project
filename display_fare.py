from connect import connect_db
from flask import render_template
import mysql.connector
from datetime import datetime
# from travel_time import map_page
from eta_test import eta

def display_fare():
    conn = connect_db()
    if conn is not None:
        try:
            # cursor = mysql.connection.cursor()
            cursor = conn.cursor()
            query_one = "SELECT route_name FROM bus_route WHERE route_name='Alpha to Foxtrot'"
            cursor.execute(query_one)
            routename_tuple = cursor.fetchone()
            routename = routename_tuple[0] if routename_tuple else None
            time_now = datetime.now()
            current_time = time_now.strftime("%H:%M:%S")

            query_two = """SELECT bus_stop.stop_name, fare.fare_amount
            FROM fare
            INNER JOIN bus_stop ON fare.stop_id=bus_stop.stop_id
            INNER JOIN time_period ON fare.time_period_id=time_period.time_period_id
            WHERE %s BETWEEN time_period.start_time AND time_period.stop_time"""
            # query="SELECT bus_stop.stop_name, fare.fare_amount FROM fare INNER JOIN bus_stop ON fare.stop_id=bus_stop.stop_id"
            # print(f"Current Time: {current_time}")
            # print(f"Query: {query_two % current_time}")
            cursor.execute(query_two, (current_time,))
            results =[
                {'stop_name':row[0],'fare_amount':row[1]} for row in cursor.fetchall()
            ]
            # print("Results:")
            # duration_text, next_stop_name = eta()
            # duration_text = '13min'
            # next_stop_name = 'Delta'
            cursor.close()
            conn.close()
            return render_template('index.html', results=results, routename=routename)
        except mysql.connector.Error as e:
            return f"Error: {e}"