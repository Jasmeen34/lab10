from sqlalchemy import Column, Integer, String, DateTime
from base import Base
class Stats(Base):
    """ Processing Statistics """
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True)
    num_temp_readings = Column(Integer, nullable=False)
    max_temp_reading = Column(Integer, nullable=False)
    num_co2_readings = Column(Integer, nullable=True)
    max_co2_reading = Column(Integer, nullable=True)
    last_updated = Column(DateTime, nullable=False)

    def __init__(self, num_temp_readings, max_temp_reading,num_co2_readings,max_co2_reading,last_updated):
        """ Initializes a processing statistics objet """
        self.num_temp_readings = num_temp_readings
        self.max_temp_reading = max_temp_reading
        self.num_co2_readings = num_co2_readings
        self.max_co2_reading = max_co2_reading
        self.last_updated = last_updated
        

    def to_dict(self):
        """ Dictionary Representation of a statistics """
        dict = {}
        dict['num_temp_readings'] = self.num_temp_readings
        dict['max_temp_reading'] = self.max_temp_reading
        dict['num_co2_readings'] = self.num_co2_readings
        dict['max_co2_reading'] = self.max_co2_reading
        dict['last_updated'] = self.last_updated.strftime("%Y-%m-%dT%H:%M:%S.%f") 
        
        return dict
    