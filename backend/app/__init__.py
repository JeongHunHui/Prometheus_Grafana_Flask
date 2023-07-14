from flask import Flask
from .db_manager import DBManager, db_manager

app = Flask(__name__)

db_manager = DBManager()

from app import routes
