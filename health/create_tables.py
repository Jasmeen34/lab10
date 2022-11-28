import sqlite3
import datetime

conn = sqlite3.connect('health.sqlite')
c = conn.cursor()
c.execute('''
        CREATE TABLE health
        (id INTEGER PRIMARY KEY ASC,
        receiver VARCHAR NOT NULL,
        storage VARCHAR NOT NULL,
        processing VARCHAR NOT NULL,
        audit VARCHAR NOT NULL,
        last_updated STRING(100) NOT NULL)
    ''')
conn.commit()
conn.close()
