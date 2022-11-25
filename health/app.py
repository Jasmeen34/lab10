import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from base import Base
import requests
from stats import Stats
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

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"
with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def check_health():
    pass

def populate_stats():
    headers = {"content-type": "application/json"}
    receiver_status  = requests.get(app_config["receiver"]['url'], headers=headers)
    storage_status = requests.get(app_config["storage"]['url'], headers=headers)
    processing_status = requests.get(app_config["processing"]['url'], headers=headers)
    audit_status = requests.get(app_config["audit"]['url'], headers=headers)

    logger.info(receiver_status.status_code)

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
    'interval',
    seconds=app_config['scheduler']['period_sec'])
    sched.start()
    

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8120)
    
    
    
    


