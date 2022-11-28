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
        CREATE TABLE health_status
        (id INTEGER PRIMARY KEY ASC,
        receiver VARCHAR NOT NULL,
        storage VARCHAR NOT NULL,
        processing VARCHAR NOT NULL,
        audit VARCHAR NOT NULL,
        last_updated STRING(100) NOT NULL)
    ''')
    conn.commit()
    conn.close()

path = 'health_status.sqlite'
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

DB_ENGINE = create_engine(f"sqlite:///{path}")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)
def check_health():
    logger.info('Request has been started')
    session = DB_SESSION()
    results = session.query(health_status).order_by(health_status.last_updated.desc())
    if not results:
        logger.error("Statistics does not exist")
        return 404

    logger.info("The request has been completed")
    session.close()
    return results[0].to_dict(), 200

def populate_stats():
    logger.info('Period processing has been started')
    session = DB_SESSION()
    headers = {"content-type": "application/json"}
    receiver_url = app_config["receiver"]['url']
    storage_url = app_config["storage"]['url']
    processing_url = app_config["processing"]['url']
    audit_url = app_config["audit"]['url']
    
    try:
        receiver_status  = requests.get(receiver_url, headers = headers)
        if receiver_status.status_code == 200:
            receiver_message = 'Running'
        else:
            receiver_message = 'Service down'
    except ConnectionError:
        receiver_message = 'Service down'
    
    try:
        storage_status =  requests.get(storage_url, headers = headers)
        if storage_status.status_code == 200:
            storage_message = 'Running'
        else:
            storage_message = 'Service down'
    except ConnectionError:
        storage_message = 'Service down'
    # try:
    #     processing_status =  requests.get(processing_url, headers = headers)
    #     logger.info(processing_url, processing_status)
    #     if processing_status.status_code == 200:
    #         processing_message = 'Running'
    #     else:
    #         processing_message = 'Service down'
    # except ConnectionError:
    processing_message = 'Service down'

    
    try:
        audit_status =  requests.get(audit_url, headers = headers)
        if audit_status.status_code == 200:
            audit_message = 'Running'
        else:
            audit_message = 'Service down'
    except ConnectionError:
        audit_message = 'Service down'
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

    health = Health(receiver_message,
        storage_message,
        processing_message,
        audit_message,
        datetime.datetime.strptime(current_timestamp,
        "%Y-%m-%dT%H:%M:%S.%f"))
    session.add(health)

    session.commit()
    session.close()
  
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
    init_scheduler()
    app.run(port=8120)
    
    
    
    


