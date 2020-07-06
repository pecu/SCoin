import json
from flask import Flask, request, render_template, jsonify
from flask_login import login_user, LoginManager, \
        UserMixin, login_required, current_user, logout_user
from flask_cors import CORS
from config import VERSION, ADMIN_ACCESS_TOKEN
from app.did import DID
from app.blockchain.tangle import find_transaction_message
from app.cb import set_layer_1, remove_layer_1
from app.token import layer_to_layer, check_token_valid, \
        get_user_balance, snapshot, get_txn_enseed
from app.cluster import check_alliance, bridge_cluster
from app.auth import check_api_key, set_user_password, \
        check_password, check_permission
from error import InvalidUsage
from utils.user import user_exist, get_total_user
from db import transaction, user

app = Flask(__name__)
CORS(app)

app.config.update(
    SECRET_KEY = ADMIN_ACCESS_TOKEN,
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

user_now = ""

class User(UserMixin):
    pass

@login_manager.user_loader  
def user_loader(username):
    user = User()  
    user.id = username
    return user

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def index():
    return 'Hello! I am the backend of light token, version: ' + VERSION

## Accounts
@app.route('/new_did', methods=['POST'])
def new_did():
    if request.method == 'POST':
        data = request.get_json()
        x_api_key = request.headers.get('X-API-key')
        
        did = DID()
        hash_bundle = did.new_did(x_api_key, data)

        return str(hash_bundle)

@app.route('/did', methods=['GET'])
def did():
    if request.method == 'GET':
        hash_did = request.args.get('hash')

        ## Read from blockchain
        content = find_transaction_message(hash_did)

    return content

## Layer-1 bank
@app.route('/set_layer1', methods=['GET'])
def set_layer1():
    if request.method == 'GET':
        ## Authentication
        x_api_key = request.headers.get('X-API-key')
        if check_permission("cb", x_api_key) == False:
            raise InvalidUsage("Authentication fail", 403)

        ## Set layer-1
        username = request.args.get('username')
        if set_layer_1(username) == False:
            raise InvalidUsage("No such account or account already exist", 400)

    return "OK"

@app.route('/remove_layer1', methods=['DELETE'])
def remove_layer1():
    if request.method == 'DELETE':
        ## Authentication
        x_api_key = request.headers.get('X-API-key')
        if check_permission("cb", x_api_key) == False:
            raise InvalidUsage("Fail at removing layer1, Authentication fail", 403)
        username = request.args.get('username')
        try:
            outcome = remove_layer_1(username)
            if outcome == False:
               raise ValueError
        except ValueError:
            raise InvalidUsage("Username hasn't been set to layer1 yet, please assign to it first", 400)
    return 'Remove ' + username

## Token
@app.route('/send_token', methods=['POST'])
def send():
    if request.method == 'POST':
        data = request.get_json()
        x_api_key = request.headers.get('X-API-key')

        if not user_exist(data["sen"]):
            raise InvalidUsage("Sender does not exist.", 404)

        # Permission check
        if check_permission(data["sen"], x_api_key) == False:
            raise InvalidUsage("Permission deny.", 403)

        # Transaction
        result = layer_to_layer(x_api_key, data)

    return result

@app.route('/get_balance', methods=['GET'])
def get_balance():
    balance = get_user_balance(request.args.get('user'))
    return balance

@app.route('/get_enseed', methods=['GET'])
def get_enseed():
    enseed = get_txn_enseed(request.args.get('hash'))
    return enseed

## Verify
@app.route('/verify_token', methods=['POST'])
def verify_token():
    if request.method == 'POST':
        data = request.get_json()
        x_api_key = request.headers.get('X-API-key')

        # Permission check
        if check_permission(data["user"], x_api_key) == False:
            raise InvalidUsage("Permission deny", 403)
        
        # Verify token
        if check_token_valid(data["user"], x_api_key, data) == True:
            return {"status":"valid"}
        else:
            return InvalidUsage("Token invalid", 400)

## Snapshot
@app.route('/snapshot', methods=['POST'])
def snapshot_token():
     if request.method == 'POST':
        data = request.get_json()
        x_api_key = request.headers.get('X-API-key')

        # Permission check
        if check_permission(data["user"], x_api_key) == False:
            raise InvalidUsage("Permission deny", 403)
        
        # snapshot
        txn_hash = snapshot(x_api_key, data)

        return txn_hash

## Get all cluster 
@app.route('/get_all_cluster', methods=['GET'])
def get_all_cluster():
    cluster = ""

    did = DID()
    cluster = did.get_cluster()

    return cluster

## Bridge
#### Different backbone:
#### 1. Use API to bridge accounts
#### 1-1. Customer API should refer the new_did API
#### 2. Re-issue token by this API
#### Same backbone:
#### 1. Use this API to new DID reference
#### 2. Re-issue token by this API

# Clutser: Layer-1 or 2 ?
#          layer-2: Currency issue
@app.route('/bridge', methods=['POST'])
def bridge():
    if request.method == 'POST':
        data = request.get_json()
        x_api_key = request.headers.get('X-API-key')

        # Chcek permission for customer CB
        if not check_alliance(data["name"], x_api_key):
            raise InvalidUsage("Not in the alliance", 400)

        # Bridge cluster
        result = bridge_cluster(data)

        return result

@app.route('/get_transactions_by_timestamp', methods=['GET'])
def get_transactions_by_timestamp():
    start = request.args.get("start")
    end = request.args.get("end")

    txns = transaction.select_by_timestamp(start, end)
    return jsonify(txns)


@app.route('/get_users_by_timestamp', methods=['GET'])
def get_users_by_timestamp():
    start = request.args.get("start")
    end = request.args.get("end")

    users = user.select_by_timestamp(start, end)
    for u in users:
        u.pop("id", None)
        u.pop("password", None)

    return jsonify(users)

@app.route('/info', methods=['GET'])
def info():
    ret = { "totalUser": get_total_user() }
    return jsonify(ret)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
