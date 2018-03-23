from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .users import *

from .chats import *

from .messages import *
