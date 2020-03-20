from flask import Flask
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()

from app import routes