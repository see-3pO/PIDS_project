import mysql.connector
from db_config import db_config
#connect to database 
def connect_db():
    conn = None
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected():
            print('Connected to database')
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return conn
    
    return conn