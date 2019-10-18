from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

api = Flask(__name__)
api.config.from_object(Config)
db = SQLAlchemy(api)
migrate = Migrate(api, db)

from api import routes, db_models
