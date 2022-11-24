
import logging
from types import new_class
import uuid
import connexion
import json
import datetime
from connexion import NoContent
import os
from swagger_ui_bundle import swagger_ui_path
import requests
import yaml
import logging
import logging.config
import random
from pykafka import KafkaClient
import time

MAX_EVENTS = 10
FILE_NAME = 'event.json'
current_retries = 0
MAX_TRIES = 10
time_in_seconds = 5

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yaml"
    log_conf_file = "/config/log_conf.yaml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yaml"
    log_conf_file = "log_conf.yaml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

with open(log_conf_file, 'r') as f:
   log_config = yaml.safe_load(f.read())
   logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

def  unique_id():
   uid = str(uuid.uuid4())
   return uid

while current_retries < MAX_TRIES:
   try:
      host = str(app_config["events"]["hostname"]) +':' +str(app_config["events"]["port"])
      client = KafkaClient(hosts=host)
      topic = client.topics[str.encode(app_config["events"]["topic"])]
      producer = topic.get_sync_producer()
      break
   except Exception as e:
      logger.debug('connection refused')
      time.sleep(time_in_seconds)
      current_retries += 1



def report_temperature_reading(body):
   uid = unique_id()
   body['trace_id'] = uid
   logger.info("Requested event temperature with a unique id of %s"%uid)
   headers = { 'content-type': 'application/json' }
   #response = requests.post(app_config['temperature']['url'], json = body, headers = headers )
   # host = str(app_config["events"]["hostname"]) +':' +str(app_config["events"]["port"])
   # client = KafkaClient(hosts=host)
   # topic = client.topics[str.encode(app_config["events"]["topic"])]
   # producer = topic.get_sync_producer()
   msg = { "type": "temperature_reading",
   "datetime" :
   datetime.datetime.now().strftime(
   "%Y-%m-%dT%H:%M:%S"),
   "payload": body }
   msg_str = json.dumps(msg)
   producer.produce(msg_str.encode('utf-8'))
   logger.info("Returned event temperature response (Id: %s) with status code %s"%(body["trace_id"], '201'))
   return NoContent, 201
    
def report_co2_reading(body):
    uid = unique_id()
    body['trace_id'] = uid
    logger.info("Requested event co2 with a unique id of %s"%uid)
    headers = { 'content-type': 'application/json' }
    #response = requests.post(app_config['co2']['url'], json = body, headers = headers )
   #  host = str(app_config["events"]["hostname"]) +':' +str(app_config["events"]["port"])
   #  logger.debug(host)
   #  client = KafkaClient(hosts=host)
   #  topic = client.topics[str.encode(app_config["events"]["topic"])]
   #  producer = topic.get_sync_producer()
    msg = { "type": "co2_reading",
   "datetime" :
   datetime.datetime.now().strftime(
   "%Y-%m-%dT%H:%M:%S"),
   "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))


    logger.info("Returned event co2 reading response (Id: %s) with status code %s"%(body["trace_id"], '201'))
    return NoContent, 201



    
app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml",
      strict_validation = True,
      validate_responses = True)
if __name__ == "__main__":
   app.run(port=8080)
