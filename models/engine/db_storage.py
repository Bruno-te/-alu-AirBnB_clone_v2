import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(f"mysql+mysqldb://{user}:{password}@{host}/{db}", pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        result = {}
        if cls:
            for obj in self.__session.query(cls).all():
                key = f"{obj.__class__.__name__}.{obj.id}"
                result[key] = obj
        else:
            for c in [State, City]:
                for obj in self.__session.query(c).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    result[key] = obj
        return result

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
