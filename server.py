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
            return "Authentication fail"

        ## Set layer-1
        username = request.args.get('username')
        set_layer_1(username)

    return "OK"

@app.route('/remove_layer1', methods=['DELETE'])
def remove_layer1():
    if request.method == 'DELETE':
        ## Authentication
        x_api_key = request.headers.get('X-API-key')
        if check_permission("cb", x_api_key) == False:
            return "Fail at removing layer1, Authentication fail"
        username = request.args.get('username')
        try:
            outcome = remove_layer_1(username)
            if outcome == False:
               raise ValueError
        except ValueError:
            return "Username hasn't been set to layer1 yet, please assign to it first"
    return 'Remove ' + username

## Token
@app.route('/send_token', methods=['POST'])
def send():
    if request.method == 'POST':
        data = request.get_json()
        x_api_key = request.headers.get('X-API-key')

        # Permission check
        if check_permission(data["sen"], x_api_key) == False:
            return {"status":"error", "msg":"Permission deny."}

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
            return {"status":"error", "msg":"Permission deny."}
        
        # Verify token
        if check_token_valid(data["user"], x_api_key, data) == True:
            return {"status":"valid"}
        else:
            return {"status":"invalid"}

## Snapshot
@app.route('/snapshot', methods=['POST'])
def snapshot_token():
     if request.method == 'POST':
        data = request.get_json()
        x_api_key = request.headers.get('X-API-key')

        # Permission check
        if check_permission(data["user"], x_api_key) == False:
            return {"status":"error", "msg":"Permission deny."}
        
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
            return {"status":"error", "msg":"Not in the alliance"}

        # Bridge cluster
        result = bridge_cluster(data)

        return result

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8888, debug = True)
