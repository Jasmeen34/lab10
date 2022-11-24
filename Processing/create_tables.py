import sqlite3
import datetime

conn = sqlite3.connect('stats.sqlite')

c = conn.cursor()
c.execute('''
    CREATE TABLE stats
    (id INTEGER PRIMARY KEY ASC,
    num_temp_readings INTEGER NOT NULL,
    max_temp_reading INTEGER NOT NULL,
    num_co2_readings INTEGER,
    max_co2_reading INTEGER,
    last_updated STRING(100) NOT NULL)
''')
conn.commit()
conn.close()