#!/usr/bin/python3
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models
from models.city import City

class State(BaseModel, Base):
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete, delete-orphan")

    @property
    def cities(self):
        if models.storage_type != "db":
            from models import storage
            return [city for city in storage.all(City).values() if city.state_id == self.id]
        return self.cities
