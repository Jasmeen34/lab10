from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class Temperature(Base):
    __tablename__ = 'temperature_reading'
    id = Column(Integer, primary_key=True)
    greenhouse_id = Column(String(250), nullable=False)
    humidity = Column(Integer, nullable=False)
    temperature_reading = Column(Integer, nullable=False)
    soil_moisture = Column(Integer, nullable=False)
    date_created = Column(String(250), nullable = False)
    trace_id = Column(String(250), nullable = False)
    date_time = Column(String(250), nullable=False)

    def __init__(self, greenhouse_id, temperature_reading, humidity, soil_moisture, trace_id,date_time):
        self.greenhouse_id = greenhouse_id
        self.temperature_reading = temperature_reading
        self.humidity = humidity
        self.soil_moisture = soil_moisture
        self.date_time = date_time
        self.trace_id = trace_id
        self.date_created = datetime.datetime.now() 

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['greenhouse_id'] = self.greenhouse_id
        dict['temperature_reading'] = self.temperature_reading
        dict['humidity'] = self.humidity
        dict['soil_moisture'] = self.soil_moisture
        dict['date_time'] = self.date_time
        dict['trace_id'] = self.trace_id
        dict['date_created'] = self.date_created

        return dict
    
