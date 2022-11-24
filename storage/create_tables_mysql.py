import mysql.connector

# db_conn = mysql.connector.connect(host="acit3855-kafka-lab6.eastus.cloudapp.azure.com", user="kafka",
# password="password", database="events",auth_plugin='mysql_native_password')
db_conn = mysql.connector.connect(host="localhost", user="root",
password="Jasmeen8$", database="events",auth_plugin='mysql_native_password')
db_cursor = db_conn.cursor()

db_cursor.execute('''
          CREATE TABLE temperature_reading
          (id INTEGER PRIMARY KEY AUTO_INCREMENT, 
           greenhouse_id VARCHAR(250) NOT NULL,
           humidity INTEGER NOT NULL,
           soil_moisture INTEGER NOT NULL,
           temperature_reading INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(250) NOT NULL,
           date_time VARCHAR(100) NOT NULL)
          ''')

db_cursor.execute('''
          CREATE TABLE co2_reading
          (id INTEGER PRIMARY KEY AUTO_INCREMENT, 
           greenhouse_id VARCHAR(250) NOT NULL,
           humidity INTEGER NOT NULL,
           soil_moisture INTEGER NOT NULL,
           co2_readings INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(250) NOT NULL,
           date_time VARCHAR(100) NOT NULL)
          ''')

db_conn.commit()
db_conn.close()

