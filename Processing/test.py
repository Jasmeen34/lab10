import connexion
from connexion import NoContent
from cv2 import split
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

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
url = app_config["temperature"]['url'] + '2016-08-29T09:12:33.001000'
print(url)
DB_ENGINE = create_engine("sqlite:///stats.sqlite")
#DB_ENGINE = create_engine("sqlite:///%s" %app_config["datastore"]["stats.sqlite"])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)
session = DB_SESSION()
results = session.query(Stats).order_by(Stats.last_updated.desc())
try :
    a = results[1]
except IndexError:
    print('a')
