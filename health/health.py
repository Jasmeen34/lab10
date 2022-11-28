from sqlalchemy import Column, Integer, String, DateTime
from base import Base
class Health(Base):
 
    __tablename__ = "health_status.py"
    id = Column(Integer, primary_key=True)
    receiver = Column(Integer, nullable=False)
    storage = Column(Integer, nullable=False)
    processing = Column(Integer, nullable=True)
    audit = Column(Integer, nullable=True)
    last_updated = Column(DateTime, nullable=False)

    def __init__(self, receiver, storage, processing, audit ,last_updated):
       
        self.receiver = receiver
        self.storage= storage
        self.procesing = processing
        self.audit = audit
        self.last_updated = last_updated
        

    def to_dict(self):
        """ Dictionary Representation of a statistics """
        dict = {}
        dict['receiver'] = self.receiver
        dict['storage'] = self.storage
        dict['processing'] = self.processing
        dict['audit'] = self.audit
        dict['last_updated'] = self.last_updated.strftime("%Y-%m-%dT%H:%M:%S.%f") 
        
        return dict
    
