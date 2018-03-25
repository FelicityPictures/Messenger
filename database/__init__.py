from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def dump_datetime(value):
    # Deserialize datetime object into string form for JSON processing
    # returns [day, time]
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

from .users import *

from .chats import *

from .messages import *
