import json
from flask import Flask
from flask_cors import CORS
from config import VERSION, ADMIN_ACCESS_TOKEN
from routes.info import info_blueprint
from routes.did import did_blueprint
from routes.token import token_blueprint
from routes.cluster import cluster_blueprint
from routes.layer import layer_blueprint
from error import InvalidUsage

app = Flask(__name__)
app.register_blueprint(info_blueprint)
app.register_blueprint(did_blueprint)
app.register_blueprint(token_blueprint)
app.register_blueprint(cluster_blueprint)
app.register_blueprint(layer_blueprint)
CORS(app)

app.config.update(
    SECRET_KEY = ADMIN_ACCESS_TOKEN,
)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def index():
    return 'Hello! I am the backend of light token, version: ' + VERSION

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
