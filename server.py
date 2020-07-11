from flask import Flask, jsonify
from flask_cors import CORS
from config import VERSION, ADMIN_ACCESS_TOKEN
from routes.info import info_blueprint
from routes.did import did_blueprint
from routes.token import token_blueprint
from routes.cluster import cluster_blueprint
from routes.layer import layer_blueprint
from routes.auth import auth_blueprint
from error import InvalidUsage

app = Flask(__name__)
app.register_blueprint(info_blueprint)
app.register_blueprint(did_blueprint)
app.register_blueprint(token_blueprint)
app.register_blueprint(cluster_blueprint)
app.register_blueprint(layer_blueprint)
app.register_blueprint(auth_blueprint)
CORS(app)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def index():
    return 'Hello! I am the backend of scoin, version: ' + VERSION

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
