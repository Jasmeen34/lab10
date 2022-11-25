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
PATH = '/data/data.sqlite'
def create_database(path):
    conn = sqlite3.connect(path)
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
file = os.path.exists('/data/data.sqlite')
if file == False:
    create_database('/data/data.sqlite')
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


DB_ENGINE = create_engine(f"sqlite:///{PATH}")
#DB_ENGINE = create_engine("sqlite:///%s" %app_config["datastore"]["stats.sqlite"])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def get_stats():
    logger.info('Request has been started')
    session = DB_SESSION()
    results = session.query(Stats).order_by(Stats.last_updated.desc())
    if not results:
        logger.error("Statistics does not exist")
        return 404

    #logger.debug(f"contents of python dictionary {results[-1].to_dict()}")
    logger.info("The request has been completed")
    session.close()
    result = results[0].to_dict()
    logger.debug(f'{result}')
    return result, 200

def populate_stats():
    """ Periodically update stats """
    headers = {"content-type": "application/json"}
    session = DB_SESSION()
    results = session.query(Stats).order_by(Stats.last_updated.desc())
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    try:
        last_updated = str(results[0].last_updated)
        a,b = last_updated.split(" ")
        url1 = app_config["temperature"]['url']+a+'T'+b +"&end_timestamp=" + current_timestamp
        url2=  app_config["co2"]['url']+a+'T'+b +"&end_timestamp=" + current_timestamp
    
    except IndexError:
        last_updated = '2016-08-29T09:12:33.001000'
        url1 = app_config["temperature"]['url']+last_updated + "&end_timestamp=" + current_timestamp
        url2=  app_config["co2"]['url'] + last_updated + "&end_timestamp=" + current_timestamp
    response1 = requests.get(url1, headers=headers)
    response2 = requests.get(url2, headers=headers)
    if response1.status_code != 200:
        logger.error(f'error status code {response1.status_code}')
    if response2.status_code != 200:
        logger.error(f'error status code {response2.status_code}')
    list1 = response1.json() 
    list2 = response2.json()
    
    try:
        num_temp_readings = results[0].num_temp_readings + len(list1)
        logger.info(f'Number of temperature readings were recieved {len(list1)}' )
        num_co2_readings  = results[0].num_co2_readings + len(list2)
        logger.info(f'Number of co2 readings were recieved {len(list2)}')
        max_temp_reading =  results[0].max_temp_reading 
        max_co2_reading = results[0].max_co2_reading
        last_updated = str(results[0].last_updated)
        a,b = last_updated.split(" ")
        url1 = app_config["temperature"]['url']+a+'T'+b +"&end_timestamp=" + current_timestamp
        url2=  app_config["co2"]['url']+a+'T'+b +"&end_timestamp=" + current_timestamp
        
    except IndexError:
        num_temp_readings = len(list1)
        num_co2_readings  = len(list2)
        max_temp_reading =  0
        max_co2_reading = 0
        last_updated = '2016-08-29T09:12:33.001000'
        url1 = app_config["temperature"]['url']+last_updated + "&end_timestamp=" + current_timestamp
        url2=  app_config["co2"]['url'] + last_updated + "&end_timestamp=" + current_timestamp
    
    logger.info('Started Periodic Processing')
    session = DB_SESSION()
    for i in list1:
        logger.debug(f'new event with a trace if of {i["trace_id"]}')
        if i["temperature_reading"] >  max_temp_reading:
            max_temp_reading = i["temperature_reading"] 
    for i in list2:
         logger.debug(f'new event with a trace if of {i["trace_id"]}')
         if i["co2_readings"] >  max_co2_reading:
            max_co2_reading = i["co2_readings"] 
    
    
    last_updated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    logger.debug(f'updated statistics num_temp_readings {num_temp_readings}, num_co2_readings {num_co2_readings}, max_temp_reading {max_temp_reading}, max_co2_reading {max_co2_reading}, {last_updated}')
    session = DB_SESSION()
    stats = Stats(num_temp_readings,
        max_temp_reading,
        num_co2_readings,
        max_co2_reading,
        datetime.datetime.strptime(current_timestamp,
        "%Y-%m-%dT%H:%M:%S.%f"))

    session.add(stats)

    session.commit()
    session.close()
    logger.info('process completed')
    return list


def health():
   return { "message": "Running"}, 200

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
    app.run(port=8100)
    
    
    

