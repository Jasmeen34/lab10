import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from base import Base
import requests
from health import Health
import yaml
import logging
import logging.config
import json
from apscheduler.schedulers.background import BackgroundScheduler
import sqlalchemy as db
from flask_cors import CORS, cross_origin
from swagger_ui_bundle import swagger_ui_path
import os
from os.path import exists
import sqlite3
import time

def create_database(path):
    conn = sqlite3.connect(path)
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

path = 'health.sqlite'
isExist = os.path.exists(path)
if isExist == True:
    print("Exists")
else:
    create_database(path)

with open("app_conf.yml", 'r') as f:
    app_config = yaml.safe_load(f.read())

with open("log_conf.yml", 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def check_health():
    pass

def populate_stats():
    headers = {"content-type": "application/json"}
    receiver = app_config["receiver"]['url']
    storage = app_config["storage"]['url']
    processing = app_config["processing"]['url']
    audit = app_config["audit"]['url']
    
    receiver_status  = requests.get(receiver, headers = headers)
    storage_status =  requests.get(storage, headers = headers)
    processing_status = requests.get(processing, headers = headers)
    audit_status = requests.get(audit, headers = headers)

    logger.info(receiver_status.status_code)

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
    'interval',
    seconds=app_config['scheduler']['period_sec'])
    sched.start()
    

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    populate_stats()
    app.run(port=8120)
    
    
    
    


