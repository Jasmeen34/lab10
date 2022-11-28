import sqlite3
import datetime

conn = sqlite3.connect('health_status.sqlite')

c = conn.cursor()
c.execute('''
    CREATE TABLE health_status
    (id INTEGER PRIMARY KEY ASC,
    receiver STRING(50) NOT NULL,
    storage  STRING(50) NOT NULL,
    processing STRING(100) NOT NULL,
    audit STRING(100) NOT NULL,
    last_updated STRING(100) NOT NULL)
''')
conn.commit()
conn.close()