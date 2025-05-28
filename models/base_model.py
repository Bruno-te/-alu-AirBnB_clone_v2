import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class BaseModel:
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.utcnow()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def save(self):
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        dict_repr = self.__dict__.copy()
        dict_repr['__class__'] = self.__class__.__name__
        if 'created_at' in dict_repr:
            dict_repr['created_at'] = self.created_at.isoformat()
        if 'updated_at' in dict_repr:
            dict_repr['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dict_repr:
            del dict_repr['_sa_instance_state']
        return dict_repr

    def delete(self):
        models.storage.delete(self)
