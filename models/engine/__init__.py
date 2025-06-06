#!/usr/bin/python3
import os

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
models.storage_type = os.getenv("HBNB_TYPE_STORAGE")
