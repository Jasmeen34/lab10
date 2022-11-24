import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE temperature_reading
          (id INTEGER PRIMARY KEY ASC, 
           greenhouse_id VARCHAR(250) NOT NULL,
           humidity INTEGER NOT NULL,
           soil_moisture INTEGER NOT NULL,
           temperature_reading INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           date_time VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE co2_reading
          (id INTEGER PRIMARY KEY ASC, 
           greenhouse_id VARCHAR(250) NOT NULL,
           humidity INTEGER NOT NULL,
           soil_moisture INTEGER NOT NULL,
           co2_readings INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           date_time VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
