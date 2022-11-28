import connexion
from connexion import NoContent
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from temperature_reading import Temperature
from co2_readings import Co2
from types import new_class
import uuid
import connexion
import json
import datetime
from connexion import NoContent
import os
from swagger_ui_bundle import swagger_ui_path
import logging
import logging.config
import random
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread 
from sqlalchemy import and_
import time

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yaml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yaml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

with open(log_conf_file, 'r') as f:
   log_config = yaml.safe_load(f.read())
   logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')
logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)
user = app_config['datastore']['user']
password = app_config['datastore']['password']
hostname = app_config['datastore']['hostname']
port = app_config['datastore']['port']
db = app_config['datastore']['db']

create_engine_str = f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}'

DB_ENGINE = create_engine(create_engine_str)
Base.metadata.bind = DB_ENGINE
Base.metadata.create_all(DB_ENGINE)
DB_SESSION = sessionmaker(bind=DB_ENGINE)


logger = logging.getLogger('basicLogger')
def report_temperature_reading(body):
    pass
    """ Receives a blood pressure reading """
    # session = DB_SESSION()

    # temp = Temperature(body['greenhouse_id'],
    #                    body['temperature_reading'],
    #                    body['humidity'],
    #                    body['soil_moisture'],
    #                    body['trace_id'],
    #                    body['date_time']
                       
                       
    # )

    # session.add(temp)

    # session.commit()
    # session.close()
    # logger.debug("Stored event - temperature request with a trace id of %s",body["trace_id"])

    # return NoContent, 201


def report_co2_reading(body):
    """ Receives a heart rate (pulse) reading """
    pass

    # session = DB_SESSION()

    # co2 = Co2(body['greenhouse_id'],
    #             body['co2_readings'],
    #                body['humidity'],
                   
    #                body['soil_moisture'],
    #                body['trace_id'],
    #                body['date_time']
    #             )

    # session.add(co2)

    # session.commit()
    # session.close()
    # logger.debug("Stored event - co2 request with a trace id of %s",body["trace_id"])
    # return NoContent, 201

    #return NoContent, 200

def get_temperature_reading(start_timestamp, end_timestamp):
    """ Gets new blood pressure readings after the timestamp """
    session = DB_SESSION()
    logger.info(create_engine_str)
    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp,  "%Y-%m-%dT%H:%M:%S.%f")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp,  "%Y-%m-%dT%H:%M:%S.%f")

    readings = session.query(Temperature).filter(and_(Temperature.date_created >= start_timestamp_datetime, Temperature.date_created < end_timestamp_datetime))
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for temperature readings after %s returns %d results" % 
    (start_timestamp, len(results_list)))
    return results_list, 200

def get_co2_reading(start_timestamp, end_timestamp):
    """ Gets new blood pressure readings after the timestamp """
    session = DB_SESSION()
    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp,  "%Y-%m-%dT%H:%M:%S.%f")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp,  "%Y-%m-%dT%H:%M:%S.%f")
    readings = session.query(Co2).filter(and_(Co2.date_created >= start_timestamp_datetime, Co2.date_created < end_timestamp_datetime))
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for temperature readings after %s returns %d results" % 
    (start_timestamp, len(results_list)))
    return results_list, 200

def process_messages():

    hostname = "%s:%d" % (app_config["events"]["hostname"],
    app_config["events"]["port"])
    maximum_retries = app_config['exception']['retry_limit']
    current_count = 0
    sleep_time = app_config['exception']['sleep']
    while current_count < maximum_retries:
        try:
           client = KafkaClient(hosts=hostname)
           topic = client.topics[str.encode(app_config["events"]["topic"])]
           consumer = topic.get_simple_consumer(consumer_group=b'event_group',
    
           reset_offset_on_start=False,
           auto_offset_reset=OffsetType.LATEST)
           for msg in consumer:
                msg_str = msg.value.decode('utf-8')
                msg = json.loads(msg_str)
                logger.info("Message: %s" % msg)
                payload = msg["payload"]
        
        
                if msg["type"] == "temperature_reading": # Change this to your event type
                # Store the event1 (i.e., the payload) to the DB
                    session = DB_SESSION()

                    temp = Temperature(payload['greenhouse_id'],
                            payload['temperature_reading'],
                            payload['humidity'],
                            payload['soil_moisture'],
                            payload['trace_id'],
                            payload['date_time'])
                    session.add(temp)
                    session.commit()
                    session.close()

                elif msg["type"] == "co2_reading": # Change this to your event type
                    session = DB_SESSION()
                    co2 = Co2(payload['greenhouse_id'],
                    payload['co2_readings'],
                    payload['humidity'],
                    payload['soil_moisture'],
                    payload['trace_id'],
                    payload['date_time']
                    )

                    session.add(co2)
                    session.commit()
                    session.close()
        # Store the event2 (i.e., the payload) to the DB
        # Commit the new message as being read
                    consumer.commit_offsets()
        except Exception as e:
    
            logger.error(f"Connection to Kafka Failed {e}")
            time.sleep(sleep_time)
            current_count += 1


def health():
   return { "message": "Running"}, 200

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    
    app.run(port=8090)

