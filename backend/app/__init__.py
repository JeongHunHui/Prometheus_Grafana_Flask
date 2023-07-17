from flask import Flask, request
from .db_manager import DBManager, db_manager
from prometheus_client import Counter, Histogram, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time

app = Flask(__name__)

db_manager = DBManager()

api_request_count = Counter('api_request_count', 'API Request Count',
                            ['method', 'status', 'endpoint'])
api_response_time = Histogram('api_response_time_seconds', 'API Response Time',
                              ['method', 'endpoint'])
api_error_count = Counter('api_error_count', 'API Error Count',
                          ['method', 'status', 'endpoint'])

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    status_code = response.status_code
    api_request_count.labels(method=request.method, status=str(status_code), endpoint=request.endpoint).inc()
    if status_code >= 400:
        api_error_count.labels(method=request.method, status=str(status_code), endpoint=request.endpoint).inc()
    elif status_code < 400:
        api_response_time.labels(method=request.method, endpoint=request.endpoint).observe(request_latency)
    return response

from app import routes
