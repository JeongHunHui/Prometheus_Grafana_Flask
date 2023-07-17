from flask import Flask
from .db_manager import DBManager, db_manager
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

db_manager = DBManager()

metrics = PrometheusMetrics(app, register_defaults=True, default_latency_as_histogram=True, excluded_methods=["OPTIONS"])

metrics.info('app_info', 'Application info', version='1.0.3')

from app import routes
