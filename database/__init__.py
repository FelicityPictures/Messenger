from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .persons import *

from .chats import *
