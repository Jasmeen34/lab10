import mysql.connector
db_conn = mysql.connector.connect(host="localhost", user="root",
password="Jasmeen8$", database="events",auth_plugin='mysql_native_password')
db_cursor = db_conn.cursor()
db_cursor.execute('''
DROP TABLE co2_reading, temperature_reading
''')
db_conn.commit()
db_conn.close()